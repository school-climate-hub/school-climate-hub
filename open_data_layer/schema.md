# Open School-Climate Data Layer — schema

The Open Data Layer is the headline open-source output of this project: a clean,
school-level, EMIS-keyed climate exposure dataset that any operator, researcher,
or government agency can build on.

**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
**Refresh cadence:** daily.
**Distribution:** GitHub release artefacts, mirrored to HDX and Zenodo.

## Tables

### `schools.csv`
The roster — primary reference table.

| Column | Type | Description |
|---|---|---|
| `emis_code` | int (PK) | National EMIS code. Globally unique within Pakistan. |
| `school_name` | string | Official school name. |
| `country` | string (ISO-3) | e.g. `PAK`. |
| `admin1` | string | Province / state. |
| `admin2` | string | District. |
| `admin3` | string | Tehsil / sub-district. |
| `operator` | string | Organisation operating the school. |
| `operator_program` | string | e.g. `PSSP`, `PSRP`. |
| `cluster` | string | Operator-defined cluster code. |
| `students` | int | Total enrolment. |
| `lat` | float | Decimal degrees, WGS84. |
| `lon` | float | Decimal degrees, WGS84. |
| `as_of` | date | Roster snapshot date. |

### `exposure_daily.parquet`
Long-format daily exposure metrics. Partitioned by year.

| Column | Type | Description |
|---|---|---|
| `emis_code` | int | FK → `schools.emis_code`. |
| `date` | date | Observation date (UTC). |
| `source` | string | `era5`, `modis_lst`, `sentinel5p`, `cams`, `glofas`. |
| `metric` | string | e.g. `t2m_max`, `t2m_min`, `lst_day`, `no2_column`, `pm25`, `flood_prob`. |
| `value` | float | Metric value (units in `data_dictionary.md`). |
| `quality` | int | 0=missing, 1=interpolated, 2=observed. |

### `exposure_school_year.parquet`
Pre-aggregated annual summaries for fast dashboards.

| Column | Type | Description |
|---|---|---|
| `emis_code` | int | FK. |
| `year` | int | Calendar year. |
| `metric` | string | e.g. `heat_stress_days`, `smog_days`, `flood_days`. |
| `agg` | string | `count`, `mean`, `p95`, `max`. |
| `value` | float | Aggregate value. |

### `vulnerability_scores.csv`
Latest scores. Refreshed nightly.

| Column | Type | Description |
|---|---|---|
| `emis_code` | int | FK. |
| `score_heat` | int (0–100) | Heat vulnerability percentile within country. |
| `score_aq` | int (0–100) | Air-quality vulnerability percentile. |
| `score_flood` | int (0–100) | Flood vulnerability percentile. |
| `score_overall` | int (0–100) | Weighted combined score. |
| `child_burden_days_yr` | int | Annual student-hazard-days. |
| `computed_at` | timestamp | Score timestamp. |

### `accreditations.csv`
Verified-only green-school programme records. Operator-declared records remain
internal until partner-attested (see v0.3 verification pipeline in ROADMAP.md).

| Column | Type | Description |
|---|---|---|
| `emis_code` | int | FK → `schools.emis_code`. |
| `type` | string | Programme code: `PGS`, `WWF`, `UGEP`, `ECO`, `PSSF`. |
| `label` | string | Human-readable programme name. |
| `source` | string | Issuing authority (e.g. `EPCCD Punjab`, `WWF-Pakistan`, `UNESCO GEP`). |
| `tier` | string | Programme tier where applicable (e.g. `Bronze`, `Silver`, `Gold`, `Green Flag`). `—` if none. |
| `year` | int | Year of accreditation / latest renewal. |
| `state` | string | Always `verified` in this file. |
| `evidence_url` | string | URL to public attestation (where available). |
| `verified_at` | timestamp | When the verification was recorded in our system. |

## Conventions

- Time zone: all dates are in UTC.
- CRS: WGS84 (EPSG:4326).
- Missing data: explicit `null` (CSV) / `NaN` (parquet), never sentinel values.
- Versioning: `vYYYY-MM-DD` git tags + GitHub releases.
