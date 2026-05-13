"""ECMWF open-data forecast ingestion via S3 mirror + byte-range reads.

Strategy:
  1. List cycle's .index files on the public S3 mirror (no auth, no rate limit).
  2. Parse JSONL index → filter to params we want (`2t`, `tp`, optionally
     `mx2t6`, `mn2t6` for daily extremes).
  3. HTTP Range-GET just those GRIB messages.
  4. Concatenate into one small .grib2 per cycle (≪ 100 MB) that downstream
     scoring opens with cfgrib/xarray.

Why not the official ecmwf-opendata client: it talks to data.ecmwf.int which
rate-limits aggressively (120s back-offs on 429s). The S3 mirror is identical
content, public, and fast.

Variables collected:
  2t   — 2m temperature, instantaneous (Kelvin)
  tp   — total precipitation, accumulated from t=0 (metres)
  mx2t6 — 6-hourly max 2m temperature (Kelvin) — only present for step ≥6
  mn2t6 — 6-hourly min 2m temperature
"""
from __future__ import annotations

import json
import shutil
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_SESSION = requests.Session()
_SESSION.mount(
    "https://",
    HTTPAdapter(
        max_retries=Retry(
            total=8,
            backoff_factor=1.5,           # 1.5, 3, 6, 12, 24, 48 s ...
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"],
            respect_retry_after_header=True,
        )
    ),
)

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "forecast"
RAW.mkdir(parents=True, exist_ok=True)

S3 = "https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com"

# Params we want — keep tight; everything else is wasted bytes.
WANT = {"2t", "tp", "mx2t6", "mn2t6"}


# ---- cycle selection ---------------------------------------------------------

def _cycle_published(cycle: str, stream: str = "oper") -> bool:
    """HEAD the step-0 GRIB to confirm the cycle is published."""
    date, hh = cycle[:8], cycle[8:10]
    url = f"{S3}/{date}/{hh}z/ifs/0p25/{stream}/{date}{hh}0000-0h-oper-fc.grib2"
    try:
        return _SESSION.head(url, timeout=10).status_code == 200
    except requests.RequestException:
        return False


def latest_cycle() -> str:
    """Most recent published 00z/12z cycle (skip 06z/18z — only 90h horizon)."""
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    # Snap to nearest 12h boundary
    now = now.replace(hour=(now.hour // 12) * 12)
    for back in range(0, 10):
        candidate = now - timedelta(hours=12 * back)
        cycle = candidate.strftime("%Y%m%d") + f"{candidate.hour:02d}"
        if _cycle_published(cycle):
            return cycle
    raise RuntimeError("No ECMWF 00z/12z cycle published in last 5 days")


# ---- step plan ---------------------------------------------------------------

def hres_steps() -> list[int]:
    """HRES 00z/12z steps: 0–144h @ 3h, then 150–240h @ 6h."""
    return list(range(0, 145, 3)) + list(range(150, 241, 6))


# ---- byte-range fetch --------------------------------------------------------

def _fetch_index(cycle: str, step: int, stream: str = "oper") -> list[dict]:
    """Fetch + parse a JSONL index file."""
    date, hh = cycle[:8], cycle[8:10]
    url = f"{S3}/{date}/{hh}z/ifs/0p25/{stream}/{date}{hh}0000-{step}h-oper-fc.index"
    r = _SESSION.get(url, timeout=30)
    r.raise_for_status()
    return [json.loads(line) for line in r.text.strip().splitlines()]


def _fetch_range(url: str, offset: int, length: int) -> bytes:
    end = offset + length - 1
    r = _SESSION.get(url, headers={"Range": f"bytes={offset}-{end}"}, timeout=60)
    if r.status_code not in (200, 206):
        r.raise_for_status()
    return r.content


def fetch_hres(cycle: str | None = None, steps: Iterable[int] | None = None) -> Path:
    """Fetch HRES — returns concatenated GRIB path."""
    cycle = cycle or latest_cycle()
    steps = list(steps) if steps is not None else hres_steps()
    out_dir = RAW / cycle
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "hres.grib2"
    if target.exists() and target.stat().st_size > 1_000_000:
        return target

    tmp = target.with_suffix(".grib2.partial")
    if tmp.exists():
        tmp.unlink()

    date, hh = cycle[:8], cycle[8:10]
    grib_url = f"{S3}/{date}/{hh}z/ifs/0p25/oper/{date}{hh}0000-{{step}}h-oper-fc.grib2"

    total = 0
    with tmp.open("wb") as fout:
        for step in steps:
            try:
                idx = _fetch_index(cycle, step)
            except requests.HTTPError as e:
                print(f"  step {step:>3}h: index missing ({e.response.status_code}) — skipping")
                continue
            wanted = [e for e in idx if e.get("param") in WANT and e.get("levtype") == "sfc"]
            if not wanted:
                continue
            url = grib_url.format(step=step)
            for entry in wanted:
                blob = _fetch_range(url, entry["_offset"], entry["_length"])
                fout.write(blob)
                total += len(blob)
                time.sleep(0.1)  # be polite to the S3 mirror
            print(f"  step {step:>3}h: {len(wanted)} fields, running total {total/1e6:.1f} MB")

    shutil.move(tmp, target)
    return target


if __name__ == "__main__":
    cycle = latest_cycle()
    print(f"ECMWF cycle: {cycle}")
    out = fetch_hres(cycle)
    print(f"HRES: {out} ({out.stat().st_size/1e6:.1f} MB)")
