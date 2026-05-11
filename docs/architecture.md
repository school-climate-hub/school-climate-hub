# Architecture

## One-page picture

```
                        ┌──────────────────────────────┐
                        │   School Roster (EMIS-keyed) │
                        │   data/schools/*.csv         │
                        └──────────────┬───────────────┘
                                       │ (lat, lon, EMIS, enrolment)
                                       ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  ERA5    │  │  MODIS   │  │ Sentinel │  │   CAMS   │  │  GloFAS  │
   │ (ECMWF)  │  │   LST    │  │   -5P    │  │  (Copern)│  │  (flood) │
   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
        │             │             │             │             │
        └─────────────┴──────┬──────┴─────────────┴─────────────┘
                             │  ingestion/*.py
                             ▼
                  ┌─────────────────────────┐
                  │  DuckDB warehouse       │
                  │  (parquet on disk)      │
                  │  exposure_daily,        │
                  │  exposure_school_year   │
                  └────────┬────────────────┘
                           │
        ┌──────────────────┼──────────────────────────┐
        │                  │                          │
        ▼                  ▼                          ▼
  ┌──────────┐    ┌─────────────────┐      ┌────────────────────┐
  │ scoring/ │    │ open_data_layer │      │  advisory/         │
  │ vuln +   │    │  Daily CSV /    │      │  daily forecast →  │
  │ burden   │    │  parquet export │      │  EN/UR/PA text     │
  └────┬─────┘    └────────┬────────┘      └─────────┬──────────┘
       │                   │                         │
       └─────────┬─────────┴─────────┐               │
                 ▼                   ▼               ▼
         ┌──────────────┐    ┌────────────────┐  ┌─────────────┐
         │ FastAPI      │    │ Public dataset │  │ SMS/WhatsApp│
         │ JSON API     │    │ (CC BY 4.0)    │  │ sink (stub) │
         └──────┬───────┘    └────────────────┘  └─────────────┘
                │
                ▼
         ┌──────────────┐
         │  Dashboard   │
         │  (Next.js,   │
         │  MapLibre)   │
         └──────────────┘
```

## Components

### School roster (`data/schools/`)
Source of truth for the deployment. CSV with EMIS code as primary key, plus
school name, project tag, cluster, tehsil, district, enrolment, lat/lon.

The PSSP/PSRP starter set (50 schools, Gujranwala) is committed to the repo.
The schema is operator-agnostic — any school operator with EMIS codes and
coordinates can drop in their own roster.

### Ingestion (`ingestion/`)
One Python module per upstream source. Each module:
- knows its API / S3 prefix / OPeNDAP endpoint;
- given the school roster, pulls daily data for the bounding box of all schools;
- writes a parquet partition to the DuckDB warehouse keyed by `(emis_code, date)`.

Idempotent. Designed to be re-runnable daily by a cron or GitHub Action.

### DuckDB warehouse
Single-file analytical DB on disk. Tables:
- `school` — roster
- `exposure_daily(emis_code, date, source, metric, value)` — long-format daily metrics
- `exposure_school_year(emis_code, year, metric, agg, value)` — pre-aggregated annual summaries

Why DuckDB: small enough to ship in the repo, fast enough for the dashboard,
SQL-queryable by external analysts without infrastructure.

### Scoring (`scoring/`)
Two outputs per school:
1. **Vulnerability scores** — 0–100 per hazard (heat, AQ, flood, rainfall),
   computed against the historical distribution of that school's exposure.
2. **Child-burden estimator** — student enrolment × historical exposure-days,
   giving an aggregate "child-hazard-day" count per cluster / district / nation.

The child-burden number is the headline UNICEF metric: it converts opaque
climate data into a unit reviewers can compare across populations.

### Open Data Layer (`open_data_layer/`)
The single most important output of this project. Daily refresh produces:
- `schools.csv` — roster
- `exposure_daily.parquet` — full daily exposure history
- `exposure_school_year.parquet` — annual summaries
- `vulnerability_scores.csv` — current scores
- `data_dictionary.md` — field-by-field documentation

Published under CC BY 4.0. Hosted as a GitHub release artefact + mirror to
HDX (Humanitarian Data Exchange) and Zenodo for permanent DOI.

### Advisory engine (`advisory/`)
Template-driven content generator. Inputs:
- daily forecast (heat, AQ, rainfall) at school location;
- school context (enrolment, age range, language profile);
- thresholds (school-day, advisory, closure-recommended).

Outputs language-tagged plain-text advisories. The SMS/WhatsApp sink is
stubbed — operators plug in their own messaging gateway and parent contact
list. The engine itself never sees parent PII.

### Dashboard (`dashboard/`)
Next.js front-end. Map of schools coloured by current vulnerability, filter
sidebar, school detail panel, child-burden headline numbers, advisory preview.

Deploys to Vercel/Netlify. Read-only over the JSON API. No auth in v1
(the data is public); v2 adds per-operator login for editing rosters.

## What's *not* in v1

- Real attendance × climate ML model. Requires daily attendance time-series
  from school-management systems; not in scope for the prototype.
  Data warehouse is structured to bolt this on later without rework.
- IoT classroom sensors. Procurement risk + maintenance overhead too high
  for a prototype; satellite + reanalysis data is sufficient for v1.
- Live school-closure decision tool. Politically sensitive; closures are a
  government call, not a tool's call. We surface evidence, we don't decide.

## Open-source choices

- **License: Apache-2.0** for code, **CC BY 4.0** for the dataset. Apache's
  patent grant clause matters for grant-funded work distributed widely.
- **No CLA** in v1. Contributors own their contributions; project is
  governed by `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md`.
- **Public-data only**: nothing in the repo or release artefacts depends
  on PDLC's private SIS, parent contacts, or any other PII. Operators
  layer their own data on top via the open schema.

## Submission notes (UNICEF Venture Fund 2026)

- Repo URL, demo URL, demo video URL go into the submission.
- "Working prototype" requirement met by the dashboard + open dataset.
- "Open source commitment" met by Apache-2.0 + CC BY 4.0 + public repo
  before submission date.
- Founding deployment (50 PDLC schools, Gujranwala) is the operational
  evidence; expansion path to all of PDLC's footprint + other operators
  is the scale narrative.
