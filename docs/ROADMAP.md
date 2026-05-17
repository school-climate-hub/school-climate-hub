# Roadmap — School Climate Hub

**Status:** Draft v0.1 · 2026-05-15
**Owners:** Reza Malik (BT) · Erum Rabbani (PDLC)

This roadmap is the time-phased plan behind [REQUIREMENTS.md](./REQUIREMENTS.md). It expands [PRD §10](./PRD.md) with concrete milestones, exit criteria, and dependencies. Dates beyond v0.1 are directional and assume UNICEF VF funding.

---

## Phase overview

| Phase | Window | Theme | Funding gate |
|---|---|---|---|
| **v0.1 — Submission** | now → 2026-05-17 | PDLC pilot proves the architecture | Self-funded (BT + PDLC) |
| **v0.2 — SaaS go-live** | 2026-06 → 2026-12 | Multi-tenant; hosted free SaaS; real dispatch | UNICEF VF Phase 1 |
| **v0.3 — Parent reach** | 2027 H1 | Public PWA; subscriptions; voluntary tenant data | Phase 2 / partnerships |
| **v0.4 — Sustainability & scale** | 2027 H2 → 2028 | Premium tier, federation, ML, regional rollout | Mixed: grants + paid licences |
| **v0.5 — Governance handover** | 2028+ | Foundation spin-out | Mixed |

---

## v0.1 — Submission (now → 2026-05-17)

**Goal:** ship a credible single-tenant PDLC pilot + open dataset schema + complete doc set, by the 2026-05-17 UNICEF VF deadline. Premier DLC is the primary applicant; BT is secondary technical implementor.

### Milestones

| Date | Milestone |
|---|---|
| 2026-05-14 | Q2/Q3 resolved: roster final, ML deferral confirmed |
| 2026-05-15 | Q1/Q4/Q5 resolved: Punjabi advisory native review, Green Schools Sindh methodology, demo video brief |
| 2026-05-16 | Q6 resolved: PDLC signs cover letter; public demo URL live; open dataset published to GitHub Releases |
| **2026-05-17** | **Submission filed by PDLC** |

### Deliverables
- Operator Console (50-school single tenant), Open Data Layer schema + first release, advisory engine with mock content in 3 languages.
- **Accreditations surface** — curated verified records for PGS, WWF, UGEP, ECO, PSSF rendered as chips on the Schools matrix + Overview rail, and as a full inline card in the school drawer. Explainer card in About.
- Docs: README, PRD, REQUIREMENTS, ROADMAP, architecture, ONBOARDING, ACCESS-CONTROL, DISCLAIMER.
- Demo video + UNICEF submission package PDF.

### Exit criteria
All [REQUIREMENTS §7](./REQUIREMENTS.md) acceptance checks tick. Submission acknowledged by UNICEF VF portal.

---

## v0.2 — Grant Phase 1: SaaS go-live (2026-06 → 2026-12)

**Goal:** turn the pilot into a multi-tenant hosted product at `schoolclimatehub.org`, plus a self-host distribution. Conditional on UNICEF VF Phase 1 funding.

### Workstreams
- **Multi-tenant rewrite** — tenant model, Postgres RLS, ABAC, per-tenant ingest config.
- **Self-service operator onboarding** — T2 verification workflow (see [ONBOARDING.md](./ONBOARDING.md)), including conflict resolution for overlapping operator claims.
- **Hosted free SaaS** — `schoolclimatehub.org`; static front-end + stateless API + cron ingest.
- **Self-host distribution** — Docker Compose bundle; `make up` brings up ingest + API + dashboard.
- **Live LLM chat** — Claude tool-use against real tenant data; citation-grounded.
- **Real dispatch** — SMS / WhatsApp / school PA gateway integrations, behind operator approval.
- **Audit-log persistence** — durable storage, export to operator on demand.
- **Operations** — observability, SLOs (ingest freshness, dashboard LCP, dispatch latency), runbooks.

### Exit criteria
- ≥ 3 verified operators (T2) onboarded outside PDLC.
- Live dispatch in production for ≥ 1 tenant.
- Open dataset mirrored to HDX and Zenodo.
- 99.5% monthly ingest success across all enabled sources per tenant.

---

## v0.3 — Parent reach (2027 H1)

**Goal:** put the data into parents' hands directly, and open the voluntary tenant-data ingestion path.

### Workstreams
- **Parent / student PWA** — phone-OTP subscriptions; any school, any tenant; no identity verification.
- **Channels** — web push + SMS + WhatsApp; multilingual auto-detect.
- **Voluntary tenant data ingest** — opt-in attendance, infrastructure status, health-incident counts; student PII stripped pre-ingest; k-anonymised cross-tenant aggregates.
- **Accreditations verification pipeline** — partner-attested verification flow (EPCCD Punjab, WWF-Pakistan, UNESCO GEP). Operator-declared records become eligible for public surfacing once a partner authority confirms. Bulk import of historical accreditation rosters from each authority.
- **Trust & safety** — abuse reporting, rate limits on advisory subscriptions, transparent data-use page.

### Exit criteria
- PWA live with ≥ 10,000 parent subscribers across pilot tenants.
- At least one tenant contributing voluntary attendance data under signed DPA.
- Public dashboard of aggregate (not per-school) health-incident trends.

---

## v0.4 — Sustainability & scale (2027 H2 → 2028)

**Goal:** prove the dual-model economics and the climate-attendance ML thesis; expand geographically.

### Workstreams
- **Premium tier** for OECD operators (paid; underwrites OSS / free-SaaS).
- **White-label + federation** for ministries — sovereign deployments contributing to a federated dataset.
- **Geographic expansion** — Sindh, KPK, Bangladesh, ROSA-wide.
- **First ML model** — climate → attendance, trained on contributed tenant data; published under CC BY 4.0 with model card.
- **UNICEF alignment** — plug into RGSP, CCRI, WCA Green Schools, Pakistan CARE, Greening Education Partnership where invited.

### Exit criteria
- ≥ 1 paying premium tenant covering ≥ 25% of run-rate.
- ≥ 1 ministry-scale federated deployment in production.
- ML model published with reproducible training pipeline and external validation note.

---

## v0.5 — Governance handover (2028+)

**Goal:** put the project beyond BT and PDLC. Foundation or independent non-profit; multi-stakeholder board (operators, child-health experts, technical advisors); commercial sustainability via mixed grants + paid licences + donations. Code stays Apache-2.0; dataset stays CC BY 4.0; brand and infrastructure pass to the foundation.

---

## Cross-cutting tracks

- **Documentation** — every phase updates README, REQUIREMENTS, ROADMAP, architecture, schema docs. No silent feature additions.
- **Security & privacy** — annual review of access-control and refusal list; pen-test before v0.2 launch.
- **Open dataset cadence** — daily refresh from v0.1 onward; SLA tightens at each phase.
- **Community** — public roadmap issue tracker from v0.2; quarterly stakeholder digest from v0.3.

## Risks & dependencies

| Risk | Mitigation |
|---|---|
| UNICEF VF Phase 1 not awarded | v0.2 scope contracts to OSS self-host + PDLC tenant only; SaaS deferred |
| PEF attendance history not shared | ML deferred to v0.4; v0.3 ships without attendance signals |
| Operator claim conflicts (two operators, same school) | Resolution workflow per [ONBOARDING.md](./ONBOARDING.md) |
| Misuse of advisories as closure orders | Disclaimer + UI copy enforce "information not advice"; operator owns the decision |
| Dataset misattribution | Provenance + licence headers embedded in every artefact |

---

*Companion docs: [PRD.md](./PRD.md) · [REQUIREMENTS.md](./REQUIREMENTS.md) · [architecture.md](./architecture.md) · [ONBOARDING.md](./ONBOARDING.md) · [ACCESS-CONTROL.md](./ACCESS-CONTROL.md) · [DISCLAIMER.md](./DISCLAIMER.md).*
