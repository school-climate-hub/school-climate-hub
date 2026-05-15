# Requirements — School Climate Hub

**Status:** Draft v0.1.1 · 2026-05-15 (attendance-correlation surface added; hero metric switched to measured attendance)
**Owners:** Reza Malik (BT) · Erum Rabbani (PDLC)
**Source of truth:** distills [PRD.md](./PRD.md) into a build-ready spec. PRD governs intent; this file governs acceptance.

---

## 1. Scope

In scope for v0.1 (UNICEF VF submission, 2026-05-17):

- Operator Console for 50 PSSP/PSRP schools in Gujranwala (PDLC tenant).
- Daily climate ingest from open sources (ERA5, MODIS LST, Sentinel-5P, CAMS, GloFAS, WorldPop).
- Per-school hazard scoring (heat, air quality, flood, overall) + child-burden estimator.
- Multilingual advisory engine (EN / UR / Punjabi-Shahmukhi) with operator approval before dispatch.
- Open School-Climate Data Layer — schema + daily refresh artefact (CC BY 4.0).
- Public demo site + open dataset release.
- **Measured-attendance correlation surface**: PDLC monthly attendance aggregates (2023–2025, school-level only, anonymised by default) shown alongside modeled exposure to ground the hazard story in observed outcomes. See [methodology-attendance.md](./methodology-attendance.md) and [DISCLAIMER.md §Tenant data](./DISCLAIMER.md).

Out of scope for v0.1 — deferred to phases below: live LLM chat (now in v0.1 as auth-less prototype), real SMS/WhatsApp dispatch, climate–attendance ML / counterfactual modeling, Sindh/KPK expansion, IoT sensors, multi-tenant SaaS. Autonomous school closure is permanently out of scope — the system never closes a school.

## 2. Stakeholders & primary jobs

| Stakeholder | Job-to-be-done |
|---|---|
| District operator (PDLC) | Triage today's hazards; dispatch advisories |
| Education officer | Closure & escalation decisions |
| School principal | Confirm action taken on alert |
| Parent / guardian | Receive advisory, act on it |
| Researcher / ministry | Download open dataset |
| UNICEF reviewer | Evaluate submission |

## 3. Functional requirements

### 3.1 Roster & geography
- **FR-1** Maintain a 50-school roster keyed on EMIS code with lat/lon, enrolment, cluster (C-1…C-4).
- **FR-2** Render all schools on a Leaflet map with hazard-coloured markers; switch layer between heat / AQ / flood / overall.
- **FR-3** Filter the map and matrix by cluster.

### 3.2 Ingest & scoring
- **FR-4** Daily cron-driven ingest pipeline per upstream source; failures logged, last-success timestamp surfaced.
- **FR-5** Per-school hazard scores (heat, AQ, flood, overall) on a 0–100 scale, refreshed each ingest cycle.
- **FR-6** Overview hero metric prefers **measured attendance** (PDLC SAR 2023–2025): percentage-point change 2023 → 2025 + lost child-school-days vs the 2023 baseline. The modeled child-burden estimate (students × hazard-days) is retained as a demoted "legacy" caption beneath the hero and continues to power the per-school Burden column on the matrix. If `attendance.json` is unavailable at load time, the dashboard falls back to the modeled hero.
- **FR-7** Score explainability surface ("Why this score?") showing top contributing features.

### 3.3 Alerts & dispatch
- **FR-8** Detect active alerts at configurable thresholds (default: overall ≥ 80); rank by severity × students-affected.
- **FR-9** Dispatch modal auto-drafts advisory in EN / UR / Punjabi-Shahmukhi; operator may edit before send.
- **FR-10** Channel selector: SMS / WhatsApp / school PA gateway. Gateway integration stubbed in v0.1.
- **FR-11** "Modify school day" modal with adjustment checklist (early dismissal, water rations, indoor recess, etc.).
- **FR-12** "Defer 24h" action re-queues the alert the next day.
- **FR-13** Every dispatch and decision is audit-logged with operator ID, timestamp, channels, template version.

### 3.4 Schools matrix & drawer
- **FR-14** Sortable RAG matrix of all 50 schools; columns include scores, enrolment, last-alert timestamp.
- **FR-15** School detail drawer opens over any view; shows scores, raw exposure, explainability, recent alerts.

### 3.5 Open Data Layer
- **FR-16** Daily-refreshed dataset published per the schema in [`open_data_layer/schema.md`](../open_data_layer/schema.md).
- **FR-17** Public download of zipped bundle plus per-table parquet + csv from a stable URL.
- **FR-18** Released under CC BY 4.0; provenance + last-refresh timestamp embedded in every artefact.

### 3.6 Settings
- **FR-19** Configurable hazard thresholds per hazard (red / amber).
- **FR-20** Active-language toggle (EN / UR / Punjabi-Shahmukhi; Sindhi / Pashto stubbed).
- **FR-21** Editable advisory templates per hazard; template version recorded on each dispatch.

### 3.7 Natural-language chat (demo-grade in v0.1)
- **FR-22** `⌘K` + FAB entry points; streaming responses with tool-call display and clickable citations.
- **FR-23** Five capability buckets: query, decide, explain, draft, multilingual. Scripted demo acceptable for v0.1.

## 4. Non-functional requirements

| # | Requirement |
|---|---|
| NFR-1 | WCAG 2.2 AA: keyboard nav, visible focus rings, semantic landmarks |
| NFR-2 | i18n via `Intl.*`; school names marked `translate="no"`; RTL where applicable |
| NFR-3 | LCP < 1.5s on 3G; map renders 50 markers in a single frame |
| NFR-4 | Theme: light / dark / system; user override persisted in `localStorage` |
| NFR-5 | Reduced-motion: honour `prefers-reduced-motion: reduce` |
| NFR-6 | Privacy: no parent PII held by the hub; tenant keeps contacts in their messaging gateway |
| NFR-7 | Licensing: Apache-2.0 (code), CC BY 4.0 (open dataset) |
| NFR-8 | Deployment: stateless API, static front-end, cron-driven ingest |
| NFR-9 | Observability: every dispatch + decision audit-logged with operator ID |
| NFR-10 | Reproducibility: ingest is idempotent per (school, date, source); re-run yields identical scores |

## 5. Data requirements

- **Upstream sources** (all open / free): ERA5, MODIS LST, Sentinel-5P, CAMS, GloFAS, WorldPop. Licence + attribution preserved in every derived artefact.
- **Roster key:** EMIS code is canonical; lat/lon validated against district boundaries on import.
- **Refusal list** (we deliberately do not hold): parent contacts, student-identifying attendance, health incidents tied to individuals. See [`docs/ACCESS-CONTROL.md`](./ACCESS-CONTROL.md).
- **Voluntary tenant data** (attendance, infrastructure, health incidents) is opt-in only, stripped of student PII before ingest, k-anonymised for cross-tenant aggregates. Cross-tenant k-anonymity stays a v0.2+ goal. In v0.1 we make one narrow exception: PDLC monthly school-level attendance aggregates for the 50 pilot schools, ingested under explicit PDLC consent and published with anonymised IDs by default. See [methodology-attendance.md](./methodology-attendance.md) and [DISCLAIMER.md §Tenant data](./DISCLAIMER.md).

## 6. Access & trust tiers (preview; full spec in ONBOARDING.md)

| Tier | Who | Access |
|---|---|---|
| T0 | Public | Open dataset, public demo |
| T1 | Demo | Read-only operator console with sample tenant |
| T2 | Verified operator | Their own tenant: ingest config, dispatch, audit log |
| T3 | Federated ministry | Cross-tenant read on their jurisdiction |

## 7. Acceptance criteria (v0.1)

- [ ] Submission filed by 2026-05-17 by PDLC as primary applicant; BT as secondary technical implementor.
- [ ] Public demo URL live by 2026-05-16; all 9 jobs-to-be-done demonstrable.
- [ ] Open dataset published to GitHub Releases.
- [ ] PDLC sign-off on operator workflow + advisory text in all three languages.
- [ ] Repo carries README, LICENSE, PRD, REQUIREMENTS, ROADMAP, architecture, onboarding, access-control, disclaimer.
- [ ] No parent PII in any artefact, dump, or log.

## 8. Constraints & assumptions

- Submission applicant is **Premier DLC**; BT is technical implementor. Forms, contacts, and signatures reflect this.
- v0.1 ships single-tenant by design; multi-tenant rewrite is a v0.2 deliverable, not a v0.1 retrofit.
- All advisories require operator approval. The system surfaces, recommends, and dispatches; it never decides.
- Punjabi-Shahmukhi text requires native-speaker review before submission (PRD Q1).

## 9. Open questions

Tracked in [PRD §8](./PRD.md). Resolve Q1–Q6 before 2026-05-16.
