# Methodology — Attendance Data

**Status:** v0.1 draft, 2026-05-15
**Source dataset:** Premier DLC School Attendance Report (SAR), 2023 / 2024 / 2025
**Output artefact:** [`attendance.json`](../attendance.json)
**Generator:** [`ingestion/attendance.py`](../ingestion/attendance.py)

This note documents how we derive the measured-attendance figures shown on the dashboard and in the AI assistant. Read it before citing any of these numbers in external materials.

---

## Source

Premier DLC shared a single Excel workbook (`SAR 2023 - 2025.xlsx`) on 2026-05-13 covering monthly attendance for the schools they support. The workbook has four sheets: one per calendar year (2023, 2024, 2025) plus a `Comparison` roll-up. Each year sheet has a header row at row 3 with the structure:

| Sr | Project | C's | EMIS | School Name | (blank) | Jan | Feb | Mar | Apr | May | Aug | Sep | Oct | Nov | Dec |

Cells are decimal fractions in [0.0, 1.0] — e.g. `0.910` = 91.0% attendance for that school in that month. Summer-break months (Jun, Jul) are absent by design — Pakistan's public school year does not include them.

The source xlsx is not committed to this repository. Its SHA-256 is recorded in `attendance.json` under `meta.source_sha256` for reproducibility.

## Collection method

Attendance is recorded by school staff in monthly registers and totalled by PDLC at month-end. **This is a manual count, not a biometric one.** Known limitations:

- Recording is subject to clerical error.
- There is no external audit trail.
- The denominator is enrolment as recorded by the school, which can lag actual roster changes.

We present this data as the best available operational measurement, not as a research-grade dataset.

## Coverage

| Year | Schools (in our roster of 50) | Months present |
|---|---|---|
| 2023 | 48 | Jan, Feb, Mar, Apr, May, Aug, Sep, Oct, Nov, Dec |
| 2024 | 48 | Jan, Feb, Mar, Apr, May, Aug, Sep, Oct, Nov, Dec |
| 2025 | 50 | Jan, Feb, Mar, Apr, May, Sep, Oct, Nov, Dec |

Two schools joined the dataset only in 2025; their 2023 and 2024 entries are recorded as `null` in the JSON. The frontend renders only available lines and discloses the gap.

## Aggregates

- `aggregates.annual_mean[year]` — unweighted mean of per-school annual means, across schools present in that year.
- `aggregates.pp_change_2023_2025` — `(annual_mean[2025] − annual_mean[2023]) × 100`, rounded to 2 decimal places. This is a **percentage-point** difference, not a percentage change. Our current value is **−3.7 pp** (recomputed across the 50 pilot schools — the workbook's Comparison sheet shows −4.6 pp because it includes schools beyond our 50).
- `aggregates.lost_child_school_days_2023_baseline` — for each (school, month) present in both 2023 and 2025, `students × (att_2023 − att_2025) × school_days_per_month`, summed. `school_days_per_month` is held constant at **20**. Schools missing from 2023 are excluded from this calculation.
- `aggregates.by_cluster` — same as annual_mean but grouped by cluster (C-1…C-4).
- `aggregates.by_month_mean` — mean attendance across all 50 schools per (year, month).

Per-school records additionally include `pp_change_2023_2025` and `may_anomaly_2025_vs_3yr` for finer-grained reasoning.

## What attendance is — and isn't

Attendance is `students-present / students-enrolled`, computed monthly. It is **not**:

- Enrolment (a child can be enrolled and chronically absent).
- Retention (children who leave the school are not counted as absent — they leave the denominator).
- Drop-out rate.
- Learning outcomes.

A 4-percentage-point fall in attendance is roughly equivalent to **~20 lost school-days per child per year** at our assumed 200-school-day calendar — meaningful, but not the same as a 4-point fall in enrolment.

## Causation framing

The 2023→2025 attendance decline includes drivers that are not climate:

- Post-COVID rebound effects (with non-monotonic trajectories at school level).
- Economic shocks (Pakistan inflation, household income).
- School management changes and teacher attrition.
- Roster transitions.

We therefore present attendance as **correlated with** rising heat and climate stress, not **caused by** it. The dashboard hero, AI assistant prompt, and submission text all use *"measured attendance change"* phrasing rather than *"climate-driven decline."*

A controlled analysis (panel regression with school fixed effects, cluster fixed effects, and climate covariates) is planned for v0.2 and will be published separately with full econometric review.

## Privacy & publication posture

- **By default we publish anonymised IDs** (`school_id_01`…`school_id_50`), not EMIS codes or school names. The mapping is held privately.
- Publishing named per-school attendance requires explicit PDLC consent. The flag `meta.school_id_anonymised` in the JSON records the publication mode.
- Aggregates (`annual_mean`, `pp_change_2023_2025`, `by_cluster`, `by_month_mean`) are not identifying and are published unconditionally.
- No student-identifying data is ever ingested. All cells are school-month averages.

## Reproducing the dataset

```bash
python -m ingestion.attendance \
  --xlsx "/path/to/SAR 2023 - 2025.xlsx" \
  --out  attendance.json
```

Add `--reveal-emis` only when PDLC consent is documented.

## Open questions

- **Pre-2023 baseline.** Even 2018–2022 monthly means at cluster level would strengthen the counterfactual. *Action: ask PDLC.*
- **Sample beyond the 50.** The source workbook includes more schools than our pilot. We could compute a regional comparison if PDLC permits.
- **Biometric augmentation.** Some PDLC schools may eventually deploy attendance biometrics. When they do, fold the cleaner stream in alongside the manual register data with a `source: "biometric"` field on per-month records.
