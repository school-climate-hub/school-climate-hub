# PRD — School Climate Hub v0.1

**Status:** Draft for 2026-05-17 UNICEF Venture Fund submission
**Owner:** Reza Malik (BT) · Erum Rabbani (PDLC)
**Last updated:** 2026-05-12

---

## 1. Problem

School-level climate exposure data — heat, air quality, flood, rainfall — does not exist as a clean, open, EMIS-keyed dataset. Operators rely on district-level weather and intuition. The data needed to act, school by school, isn't there.

## 2. Users

| User | When they use it |
|---|---|
| **District operator** (Zeeshan @ PDLC) | Daily — hazard triage, advisory dispatch |
| **District education officer** | Weekly+ — closure decisions, escalations |
| **School principal** | When alerted — confirms action taken |
| **Parent / guardian** | When alerted — acts on advisory |
| **UNICEF reviewer** | One-time — evaluates the submission |
| **Researcher / NGO / ministry** | Ad-hoc — downloads the open dataset |

## 3. Jobs to be done

| ID | Job | Surface |
|---|---|---|
| J1 | What's happening across my estate right now? | Overview (map + KPIs) |
| J2 | Which schools need a decision today? | Overview (active alerts panel) |
| J3 | Send a parent advisory in 3 languages | Dispatch flow |
| J4 | Modify a school day (early dismissal, water rations) | School-day modal |
| J5 | Compare schools, drill down on one | Schools matrix → drawer |
| J6 | Understand why a school's score is high | School drawer → "Why this score?" |
| J7 | Get the underlying open dataset | Open Data view |
| J8 | Ask a natural-language question | Chat (⌘K / FAB) |
| J9 | Tune thresholds, languages, channels, templates | Settings |

## 4. Features (v0.1)

| Feature | Status |
|---|---|
| 50-school roster (Gujranwala-50), EMIS + lat/lon | ✅ |
| Daily ingest: ERA5 / MODIS LST / Sentinel-5P / CAMS / GloFAS | Code stubbed |
| Per-school hazard scoring (heat / AQ / flood / overall) 0–100 | Mock |
| Child-burden estimator (students × hazard-days) | Mock |
| Active-alert detection at configurable thresholds | Mock |
| Multilingual advisory engine (EN / UR / Punjabi-Shahmukhi) | Mock content |
| Operator approval workflow before dispatch | UI complete |
| Dispatch via SMS / WhatsApp / school PA gateway | Stubbed |
| Audit log of decisions + dispatches | Schema only |
| Open Data Layer — daily refresh, CC BY 4.0 | Schema only |
| Score explainability (SHAP-style feature attribution) | Mock |
| Natural-language chat (`⌘K`) over the data | Scripted demo |
| Theme: light / dark / system | ✅ |

## 5. Functional requirements

| # | Requirement |
|---|---|
| FR-1 | Display all 50 schools on a Leaflet map with hazard-coloured markers |
| FR-2 | Switch map layer: heat / air-quality / flood / overall |
| FR-3 | Filter by cluster (C-1 to C-4) |
| FR-4 | Show child-burden estimate as the hero metric on Overview |
| FR-5 | Surface active alerts (overall ≥80) ranked by severity × students-affected |
| FR-6 | Open dispatch modal showing auto-drafted EN/UR/PA advisory text |
| FR-7 | Channel selection (SMS / WhatsApp / school PA) before send |
| FR-8 | "Modify school day" modal with adjustment checklist |
| FR-9 | "Defer 24h" action that re-queues the alert tomorrow |
| FR-10 | RAG matrix table: all 50 schools, sortable by any column |
| FR-11 | School detail drawer: scores, exposure, explainability — opens over any view |
| FR-12 | Public download of dataset (.zip) and per-table parquet/csv |
| FR-13 | Configurable hazard thresholds (red/amber per hazard) |
| FR-14 | Active-language toggle (EN / UR / Punjabi-Shahmukhi / Sindhi / Pashto) |
| FR-15 | Editable advisory templates per hazard |
| FR-16 | Chat: `⌘K` + FAB; streaming responses; tool-call display; clickable citations |
| FR-17 | Chat: 5 capability buckets — query, decide, explain, draft, multilingual |

## 6. Non-functional requirements

| # | Requirement |
|---|---|
| NFR-1 | WCAG 2.2 AA; keyboard nav; visible focus rings on all interactive elements |
| NFR-2 | i18n: EN / UR / Punjabi-Shahmukhi; `Intl.DateTimeFormat` + `Intl.NumberFormat`; school names marked `translate="no"` |
| NFR-3 | Performance: LCP < 1.5s on 3G; map renders 50 markers in single frame |
| NFR-4 | Theme: system default; user override persisted in `localStorage` |
| NFR-5 | Privacy: no parent PII in the hub; messaging gateway holds contacts |
| NFR-6 | Licensing: Apache-2.0 (code) · CC BY 4.0 (open dataset) |
| NFR-7 | Deployment: stateless API, static front-end, cron-driven ingest |
| NFR-8 | Observability: all dispatches + decisions audit-logged with operator ID |
| NFR-9 | Reduced-motion: animations honour `prefers-reduced-motion: reduce` |

## 7. Out of scope (v0.1)

- **Climate–attendance ML model** — needs PEF SIS attendance history; deferred to Phase 1 grant deliverable
- **Live LLM-backed chat** — submission ships scripted demos; real Claude tool-use built post-funding
- **Real SMS/WhatsApp dispatch** — gateway stubbed; integrated in Phase 1
- **Sindh / KPK expansion** — pending PDLC data
- **IoT classroom sensors** — procurement risk; satellite + reanalysis is enough for v0.1
- **Autonomous school closure** — system *never* closes a school; that is a government call

## 8. Open questions / pending decisions

| # | Question | Owner | Needed by |
|---|---|---|---|
| Q1 | Final Punjabi-Shahmukhi advisory text — needs native-speaker review | PDLC | 2026-05-15 |
| Q2 | Is the 50-school footprint final, or are Sindh/KPK files coming? | Zeeshan (PDLC) | 2026-05-14 |
| Q3 | Will PEF attendance history be shared, or is the ML module deferred? | Zeeshan (PDLC) | 2026-05-14 |
| Q4 | Green School Sindh methodology document for narrative continuity | Zeeshan (PDLC) | 2026-05-15 |
| Q5 | Demo video target length and key beats | Reza (BT) | 2026-05-15 |
| Q6 | Submission package PDF — who signs the cover letter? | Erum (PDLC) | 2026-05-16 |

## 9. Success criteria

- [ ] Submission filed by **2026-05-17** by PDLC
- [ ] Public demo URL live by **2026-05-16**
- [ ] Open dataset published to GitHub Releases (target HDX + Zenodo mirror post-submission)
- [ ] All 9 jobs-to-be-done demonstrable in the live mockup
- [ ] PDLC sign-off on the operator workflow + advisory text
- [ ] Repo has README, LICENSE, PRD, architecture doc, open-dataset schema

## 10. Phase roadmap

| Phase | Window | Deliverables |
|---|---|---|
| **v0.1 — Submission** | now → 2026-05-17 | PDLC pilot proves the architecture; open dataset schema; this PRD; architecture, onboarding, access-control, disclaimer docs |
| **v0.2 — Grant Phase 1: SaaS go-live** | 2026-06 → 2026-12 (if funded) | Multi-tenant rewrite; self-service operator signup; hosted free SaaS at `schoolclimatehub.org`; self-host shipped as Docker Compose; live LLM chat; real SMS/WhatsApp dispatch; audit-log persistence |
| **v0.3 — Parent reach** | 2027 H1 | Parent/student PWA; phone-OTP subscriptions; web push + SMS + WhatsApp alerts; multilingual auto-detect; opt-in tenant data ingestion (attendance, infrastructure, health incidents) |
| **v0.4 — Sustainability + scale** | 2027 H2 → 2028 | Premium tier for OECD operators; white-label + federation for ministries; Sindh + KPK + Bangladesh + ROSA-wide rollout; first climate-attendance ML model trained on contributed data |
| **v0.5 — Governance handover** | 2028+ | Spin-out into a foundation or independent non-profit; open multi-stakeholder governance (operators, child-health experts, technical advisors); commercial sustainability via mixed grants + paid licences + donations |

## 11. Productisation strategy & UNICEF alignment

**Dual model:** open-source code + free hosted SaaS. Both first-class.

| Channel | Who it serves | Why |
|---|---|---|
| **OSS self-host** (`github.com/school-climate-hub`) | Ministries needing data residency; technical operators; researchers | Sovereignty, auditability, no vendor lock-in |
| **Free hosted SaaS** (`schoolclimatehub.org`, v0.2+) | The 99% of operators without staff to run their own deployment; parents and the public | Lowers barrier to entry; captures network-effect of cross-tenant dataset; underwrites OSS development |

This is the GitLab / Sentry / PostHog / Plausible model adapted to a children's-health public good. Code is Apache-2.0; dataset is CC BY 4.0; running infrastructure is the value-add operators pay for (or receive funded).

### Three product surfaces (not one)

- **Operator Console** (B2B/B2G) — what v0.1 builds; multi-tenant in v0.2
- **Open Data Platform** (B2D — developers, researchers, ministries) — strengthens what's there
- **Parent app PWA** (B2C, v0.3) — anyone can subscribe to any school; phone-OTP; free

### Onboarding, access control, disclaimers

- [`docs/ONBOARDING.md`](./ONBOARDING.md) — four-tier access model (T0 public · T1 demo · T2 verified operator · T3 federated ministry); verification workflow including conflict resolution for overlapping operator claims
- [`docs/ACCESS-CONTROL.md`](./ACCESS-CONTROL.md) — PII categories, role × access matrix, technical enforcement (Postgres RLS + ABAC + encryption + audit), what we deliberately refuse to hold, voluntary opt-in tenant data ingestion (attendance, infrastructure, health incidents — the long-term moat)
- [`docs/DISCLAIMER.md`](./DISCLAIMER.md) — risk profile, core legal principles ("information not advice"; operator owns the decision; best-available accuracy), required legal documents per launch phase

### Privacy posture summary

- **We never ingest parent contacts.** Tenant keeps them in their existing messaging gateway; hub fires dispatch trigger; tenant fans out.
- **Public subscribers (parent app) sign up directly.** Phone-OTP, opt-in, no identity verification ("are you a parent?" is exclusionary + unverifiable + irrelevant — broadcast data is public).
- **Voluntary tenant data** (attendance, infrastructure, health incidents) is opt-in only, stripped of student PII before ingest, k-anonymised for cross-tenant aggregates.

### UNICEF Green Schools & global infrastructure alignment

The hub is designed to plug into UNICEF's active climate-and-education infrastructure:

| Initiative | How we fit |
|---|---|
| **UNICEF Regional Green School Platform (RGSP)** — launched April 2026 in Central Asia at RES 2026; 23M children in scope | Operational infrastructure-monitoring layer for the platform's school-resilience pillar. Apache-2.0 + CC BY 4.0 makes it usable by any participating ministry without vendor negotiation. |
| **UNICEF West & Central Africa Green School Initiative** | Same fit; WCA has the highest heat-stress urgency globally. |
| **UNICEF Children's Climate Risk Index (CCRI)** | Our school-level data refines CCRI from sub-national to per-institution granularity. Direct contribution to UNICEF's flagship measurement product. |
| **UNICEF Pakistan CARE programme** (Climate Action & Resilience in Education) | PDLC pilot sits inside CARE's geographic scope; natural country-office on-ramp. |
| **UNESCO-led Greening Education Partnership** (UNICEF partner) | Open-data interoperability layer for the partnership. |

We do not claim formal partnership with these programmes; we claim architectural, licensing, and data alignment. As regional Green School platforms roll out (RGSP launched 3 weeks ago; ROSA next), the hub is ready to plug in immediately.

---

*This PRD is intentionally short. Architecture details are in [`docs/architecture.md`](./architecture.md). Open-dataset schema is in [`open_data_layer/schema.md`](../open_data_layer/schema.md). Onboarding / access / disclaimer docs are in [`docs/`](./). The current mockup is at [`mockups/dashboard.html`](../mockups/dashboard.html). Live demo at https://school-climate-hub.github.io/school-climate-hub/.*
