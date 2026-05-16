# School Climate Hub — Open Data Bundle v0.1

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
