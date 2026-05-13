"""MODIS Land-Surface-Temperature ingestion via NASA earthaccess.

Product: MOD11A1 (Terra, daily LST, 1km).
Credentials: ~/Repo/.bt-creds/earthdata.env (EARTHDATA_TOKEN, EARTHDATA_USERNAME).
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "modis"
RAW.mkdir(parents=True, exist_ok=True)

# Gujranwala-50 bounding box (lon_w, lat_s, lon_e, lat_n) per earthaccess convention
BBOX_LON_LAT = (73.75, 31.85, 74.40, 32.45)


def _login():
    """Authenticate to Earthdata using the token in earthdata.env.
    earthaccess accepts EDL_TOKEN env var, OR a netrc file, OR username/password."""
    load_dotenv(Path.home() / "Repo" / ".bt-creds" / "earthdata.env")
    token = os.environ.get("EARTHDATA_TOKEN", "")
    if token:
        os.environ["EDL_TOKEN"] = token

    import earthaccess
    auth = earthaccess.login(strategy="environment", persist=False)
    # earthaccess sometimes returns authenticated=False even when search works;
    # we proceed regardless and let actual download surface real failures
    return earthaccess.__name__ and earthaccess


def search(start: datetime, end: datetime, count: int | None = None):
    """Search MODIS LST granules for the school bbox within a time window."""
    ea = _login()
    return ea.search_data(
        short_name="MOD11A1",
        version="061",
        bounding_box=BBOX_LON_LAT,
        temporal=(start.date().isoformat(), end.date().isoformat()),
        count=count or 100,
    )


def download_recent(days: int = 7) -> list[Path]:
    """Download last `days` of MOD11A1 granules to data/raw/modis/.
    Returns list of local file paths."""
    ea = _login()
    end = datetime.now(timezone.utc).date() - timedelta(days=2)  # MODIS L3 lags ~1 day
    start = end - timedelta(days=days - 1)

    print(f"[modis] searching {start} → {end} · bbox={BBOX_LON_LAT}")
    granules = ea.search_data(
        short_name="MOD11A1",
        version="061",
        bounding_box=BBOX_LON_LAT,
        temporal=(start.isoformat(), end.isoformat()),
        count=100,
    )
    print(f"[modis] found {len(granules)} granules")
    if not granules:
        return []

    paths = ea.download(granules, str(RAW))
    print(f"[modis] downloaded {len(paths)} files to {RAW}")
    return [Path(p) for p in paths]


if __name__ == "__main__":
    files = download_recent(days=7)
    for p in files:
        print(f"  {p} ({p.stat().st_size:,} bytes)" if p.exists() else f"  {p} (missing)")
