"""ERA5 ingestion — pulls recent surface variables for the Gujranwala-50 bounding box.

Uses Copernicus Climate Data Store (CDS) API via cdsapi.
Credentials in ~/Repo/.bt-creds/cds.env (CDSAPI_URL, CDSAPI_KEY).
Dataset T&Cs must be accepted once at:
  https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
"""
from __future__ import annotations

import os
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import cdsapi
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# Gujranwala-50 bounding box with small padding (degrees)
# North-West, South-East corners; CDS uses [N, W, S, E]
BBOX = [32.45, 73.75, 31.85, 74.40]  # N, W, S, E

VARIABLES = [
    "2m_temperature",          # heat — Kelvin
    "total_precipitation",     # rainfall — metres per hour, accumulated
    "2m_dewpoint_temperature", # for heat-index later
]


def load_credentials() -> tuple[str, str]:
    """Load CDS URL + key from ~/Repo/.bt-creds/cds.env."""
    load_dotenv(Path.home() / "Repo" / ".bt-creds" / "cds.env")
    url = os.environ.get("CDSAPI_URL")
    key = os.environ.get("CDSAPI_KEY")
    if not url or not key:
        raise RuntimeError("CDS credentials missing — check ~/Repo/.bt-creds/cds.env")
    return url, key


def submit_recent(days: int = 7) -> Path:
    """Submit a CDS request for the last `days` of hourly ERA5 over the school bbox.
    Returns the destination path; blocks until CDS delivers the file."""
    url, key = load_credentials()
    client = cdsapi.Client(url=url, key=key, quiet=False)

    end = datetime.now(timezone.utc).date() - timedelta(days=1)  # ERA5 lags by ~5 days but try recent
    start = end - timedelta(days=days - 1)
    dates = [start + timedelta(days=i) for i in range(days)]

    request = {
        "product_type": ["reanalysis"],
        "variable": VARIABLES,
        "year": sorted({f"{d.year}" for d in dates}),
        "month": sorted({f"{d.month:02d}" for d in dates}),
        "day": sorted({f"{d.day:02d}" for d in dates}),
        "time": [f"{h:02d}:00" for h in range(24)],
        "area": BBOX,   # N, W, S, E
        "data_format": "netcdf",
        "download_format": "unarchived",
    }

    dest = RAW / f"era5_recent_{start.isoformat()}_to_{end.isoformat()}.nc"
    print(f"[era5] requesting: {start} → {end} · vars={len(VARIABLES)} · bbox={BBOX}")
    print(f"[era5] dest:       {dest}")
    client.retrieve("reanalysis-era5-single-levels", request, str(dest))
    print(f"[era5] downloaded {dest.stat().st_size:,} bytes")

    # CDS multi-step-type requests return a ZIP of one-or-more .nc files.
    # If so, extract to a sibling directory and return that.
    if zipfile.is_zipfile(dest):
        extract_dir = dest.with_suffix("")
        extract_dir.mkdir(exist_ok=True)
        with zipfile.ZipFile(dest) as z:
            z.extractall(extract_dir)
        ncs = sorted(extract_dir.glob("*.nc"))
        print(f"[era5] extracted {len(ncs)} NetCDFs to {extract_dir}")
        return extract_dir
    return dest


if __name__ == "__main__":
    out = submit_recent(days=7)
    print(f"\nSuccess: {out}")
