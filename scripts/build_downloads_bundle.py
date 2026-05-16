"""Build the Open Data downloads bundle (/downloads/scs-v0.1.zip).

Pulls together the live data artefacts and packages them with licence + readme.
Re-run after each scoring/ingestion refresh.

Outputs:
    downloads/scs-v0.1.zip                            (one-shot full bundle)
    downloads/schools.csv, scores.csv, attendance_aggregates.csv  (per-file)
    downloads/README.md, LICENSE.md                   (legalese alongside the data)

The .json originals at the repo root are the canonical machine-readable surface;
the .csv conversions are operator-friendly secondary downloads.
"""
from __future__ import annotations

import csv
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "downloads"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "schools.json": ROOT / "schools.json",
    "scores.json": ROOT / "scores.json",
    "attendance.json": ROOT / "attendance.json",
}

README = """# School Climate Hub — Open Data Bundle v0.1

A clean, school-level, EMIS-keyed climate-exposure dataset for the 50 pilot
schools managed by Premier DLC in Gujranwala, Pakistan.

Live data also available via:
  https://schoolclimatehub.org/schools.json
  https://schoolclimatehub.org/scores.json
  https://schoolclimatehub.org/attendance.json

## Contents

  schools.json / schools.csv                Roster: 50 schools with EMIS code,
                                            cluster, tehsil, students, lat/lon.
  scores.json                               Current per-school hazard scores +
                                            10-day ECMWF HRES forecast +
                                            15-day ECMWF ENS probabilistic.
  scores.csv                                Flat per-school current scores.
  attendance.json                           Measured monthly attendance from
                                            Premier DLC's School Attendance
                                            Reports, 2023–2025. School IDs are
                                            anonymised by default (school_id_01
                                            ..50); aggregates are non-identifying.
  attendance_aggregates.csv                 Annual means per anonymised school
                                            id + the 2023→2025 pp change.

## Licence

Dataset is CC BY 4.0. Code that produces the dataset is Apache-2.0.
See LICENSE.md for full text.

Required citation:
  School Climate Hub (Beaconhouse Technology + Premier DLC, 2026),
  Pakistan school-level climate exposure dataset v0.1, CC BY 4.0.

## Disclaimers

  - Data may contain inaccuracies, latency, or gaps. Not for medical, legal,
    or safety decisions. See https://schoolclimatehub.org for the live demo
    and full risk framework (docs/DISCLAIMER.md in the repo).
  - Attendance is presented as a *correlated outcome*, not a climate-caused
    decline. The 2023→2025 fall reflects post-COVID, economic, and management
    drivers alongside climate. See docs/methodology-attendance.md.
  - Per-school named publication requires explicit Premier DLC consent. The
    bundle ships anonymised by default.

## Repository

https://github.com/school-climate-hub/school-climate-hub
"""

LICENCE = """# Licence

## Code (in the source repository)
Apache License 2.0
https://www.apache.org/licenses/LICENSE-2.0

## Dataset (this bundle)
Creative Commons Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/

You are free to:
  - Share — copy and redistribute the material in any medium or format
  - Adapt — remix, transform, and build upon the material for any purpose

Under the following terms:
  - Attribution — You must give appropriate credit, provide a link to the
    licence, and indicate if changes were made. Suggested citation:

      School Climate Hub (Beaconhouse Technology + Premier DLC, 2026).
      Pakistan school-level climate exposure dataset v0.1. CC BY 4.0.

  - No additional restrictions — You may not apply legal terms or
    technological measures that legally restrict others from doing anything
    the licence permits.

No warranties are given. The licence may not give you all of the permissions
necessary for your intended use. For example, other rights such as publicity,
privacy, or moral rights may limit how you use the material.
"""


def write_schools_csv():
    data = json.loads(SOURCES["schools.json"].read_text())
    cols = ["emis_code", "school_name", "cluster", "tehsil", "students", "lat", "lon"]
    rows = data["schools"] if isinstance(data, dict) and "schools" in data else data
    with (OUT / "schools.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_scores_csv():
    data = json.loads(SOURCES["scores.json"].read_text())
    cols = ["emis_code", "school_name", "cluster", "students",
            "heat", "aq", "flood", "overall",
            "t2m_max_c", "precip_24h_mm_max", "burden_days_per_year"]
    with (OUT / "scores.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for s in data.get("schools", []):
            sc = s.get("scores", {}); raw = s.get("raw", {})
            w.writerow([
                s.get("emis_code"), s.get("school_name"), s.get("cluster"),
                s.get("students"),
                sc.get("heat"), sc.get("aq"), sc.get("flood"), sc.get("overall"),
                raw.get("t2m_max_c"), raw.get("precip_24h_mm_max"),
                s.get("burden_days_per_year"),
            ])


def _csv_escape(v):
    # CSV-injection guard
    if isinstance(v, str) and v and v[0] in "=+-@\t\r":
        return "'" + v
    return v


def write_attendance_aggregates_csv():
    data = json.loads(SOURCES["attendance.json"].read_text())
    schools = data.get("schools", {})
    cols = ["school_id", "cluster", "students",
            "mean_2023", "mean_2024", "mean_2025", "pp_change_2023_2025",
            "may_anomaly_2025_vs_3yr"]
    with (OUT / "attendance_aggregates.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for sid, rec in schools.items():
            am = rec.get("annual_mean", {})
            w.writerow([_csv_escape(sid), rec.get("cluster"), rec.get("students"),
                        am.get("2023"), am.get("2024"), am.get("2025"),
                        rec.get("pp_change_2023_2025"),
                        rec.get("may_anomaly_2025_vs_3yr")])


def write_readme_and_licence():
    (OUT / "README.md").write_text(README)
    (OUT / "LICENSE.md").write_text(LICENCE)
    methods_src = ROOT / "docs" / "methodology-attendance.md"
    if methods_src.exists():
        shutil.copy2(methods_src, OUT / "methodology-attendance.md")


def build_zip():
    zip_path = OUT / "scs-v0.1.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for fname in ["README.md", "LICENSE.md", "methodology-attendance.md",
                      "schools.csv", "scores.csv", "attendance_aggregates.csv"]:
            p = OUT / fname
            if p.exists():
                z.write(p, arcname=fname)
        for fname, src in SOURCES.items():
            if src.exists():
                z.write(src, arcname=fname)
    return zip_path


def main():
    write_schools_csv()
    write_scores_csv()
    write_attendance_aggregates_csv()
    write_readme_and_licence()
    zp = build_zip()
    print(f"wrote {zp} ({zp.stat().st_size / 1024:.1f} KB)")
    print(f"contents:")
    for f in sorted(OUT.iterdir()):
        print(f"  {f.name:36}  {f.stat().st_size / 1024:>6.1f} KB")


if __name__ == "__main__":
    main()
