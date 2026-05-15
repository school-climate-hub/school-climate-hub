# Legal disclaimers & risk framework

How the School Climate Hub limits and allocates risk while staying useful.

> ⚠️ **This document is a working draft of legal principles, not lawyer-reviewed terms.** Before the SaaS launches publicly, the actual Terms of Service, Privacy Policy, AUP, DPA, and Operator Agreement must be drafted (or reviewed) by qualified counsel in the relevant jurisdictions (US, UK, EU, Pakistan, India to start).
>
> The language here is honest and operator-friendly; it captures the *intent* the formal docs must express.

---

## Risk profile — what we're protecting against

| Risk | How it could play out | Mitigation |
|---|---|---|
| **Failure-to-warn liability** | Operator dispatches advisory based on our score; advisory was wrong direction; child harmed; family sues us. | Clear disclaimer (information, not advice); operator owns dispatch decision; limitation of liability. |
| **Data accuracy claims** | Score turns out to be wrong due to upstream satellite latency; operator misallocated resources. | "Best-available accuracy" framing; explicit forecast uncertainty; no warranty. |
| **Cross-tenant data leak** | Bug exposes one operator's data to another. | Architecture-level isolation (RLS); audit logs; incident-response policy. |
| **Parent app PII breach** | Our subscriber database compromised. | Minimal data collected; encrypted at rest; rapid notification per regulation. |
| **Misuse by operator** | Tenant uses platform to mis-direct, intimidate, or surveil parents. | AUP prohibits; verification at T2; revocation on breach. |
| **Misuse by us** | Future commercial pressure to monetise data inappropriately. | Foundation governance; charter restrictions; OSS makes harmful pivots forkable. |
| **Liability for self-host failures** | Someone self-hosts, it breaks, they blame us. | OSS license disclaims warranty; clear separation between hosted SaaS and self-host. |
| **Regulatory action** | GDPR / DPDP / PECA / COPPA fine for non-compliance. | Privacy-by-architecture; counsel review per jurisdiction; data residency options. |

---

## Core legal principles

These principles must show up — in some form — in every public-facing document.

### 1. Information, not advice
> "Hazard scores and forecasts shown on this platform are informational. They do not constitute medical, safety, operational, legal, or any other form of advice. The platform is a decision-support tool, not a decision-maker."

### 2. Operator owns the decision
> "School closure, dispatch, school-day modification, and child-welfare decisions are made by the operating organisation, the school, the relevant government authority, or the parent. The platform does not take operational actions on behalf of users."

(This is already true in our architecture — the system never closes a school or dispatches without operator approval.)

### 3. Best-available accuracy, no guarantee
> "Climate and exposure data are sourced from public providers (ERA5, MODIS, Sentinel-5P, CAMS, GloFAS) and may contain inaccuracies, latency, gaps, or outages. Scores are estimates with inherent uncertainty. The platform makes no warranty of accuracy, completeness, or fitness for any particular purpose."

### 4. Forecast uncertainty
> "Forecasts indicate likelihood, not certainty. Actual conditions may diverge significantly. Decisions should account for forecast uncertainty."

### 5. No duty to act
> "The platform does not warrant that alerts will be delivered, that operators will act on them, that any action will prevent harm, or that the platform itself will be available without interruption."

### 6. Limitation of liability
> "To the maximum extent permitted by applicable law, the platform's total liability to any user is limited to the fees paid by that user in the twelve months preceding the claim. For free-tier and public-tier users, total liability is limited to USD 100. The platform is not liable for indirect, incidental, consequential, or punitive damages."

### 7. Operator indemnification
> "Operators agree to indemnify, defend, and hold harmless the platform from any claim arising from: (a) the operator's use of the platform, (b) the operator's dispatch or failure to dispatch, (c) the operator's decisions about school operations, (d) the operator's breach of the Acceptable Use Policy."

### 8. Subscriber acknowledgement
> "By subscribing to alerts about a school, you acknowledge that: alerts may be delayed or fail to deliver; alerts are based on forecasts with inherent uncertainty; alerts are not a substitute for direct communication with your child's school; and the platform is not responsible for actions taken or not taken in response to alerts."

### 9. Jurisdiction
> "These terms are governed by the laws of [TBD — see below]. Disputes are resolved in [TBD]."

Likely options:
- **Delaware, US** — if BT or a US-incorporated entity holds the platform
- **England & Wales** — if a UK foundation holds it
- **Singapore** — for genuinely international open-source projects with global reach
- **Mandatory arbitration vs court** — TBD; arbitration is faster and cheaper, but optics matter for a children's-health platform

### 10. Right to be forgotten
> "Subscribers may delete their accounts and have all personal data erased within 30 days. Operators may export all their tenant data and request deletion. Audit logs may be retained beyond user deletion where required by law or for security-incident investigation."

---

## Required legal documents

### For v0.2 SaaS launch (must exist before any public signup)

| Doc | Audience | Status |
|---|---|---|
| **Terms of Service** | All users | Draft (this doc) — must be lawyer-finalised |
| **Privacy Policy** | All users (esp. parent app) | Must comply with GDPR · India DPDP · Pakistan PECA · US COPPA |
| **Acceptable Use Policy** | All users | Plain-language list of dos/don'ts |
| **Cookie Policy** | Web users | Simple — we use minimal cookies |
| **Open Data License** | Public dataset users | CC BY 4.0 + disclaimer addendum |
| **Operator Agreement** | T2/T3 operators | Additional duties: roster accuracy, dispatch oversight, audit cooperation |

### For v0.3 (parent app)

| Doc | Audience |
|---|---|
| **Subscriber Terms** | Parent-app PWA users |
| **Children's Privacy Notice** | If under-13 subscribers permitted in any jurisdiction (likely opt-out by default in COPPA / GDPR-K regions) |

### For T3 ministry deployments

| Doc | Audience |
|---|---|
| **Data Processing Agreement (DPA)** | GDPR Art. 28 + India DPDP equivalent |
| **Master Services Agreement** | Custom contract per ministry |
| **Standard Contractual Clauses** | Where EU/UK data crosses borders |
| **Country-specific addenda** | Per jurisdiction |

---

## Plain-language disclaimer (for use in product)

The actual text shown in the dashboard footer and the parent app:

> **This is decision-support, not advice.**
> Operators decide what to do; we surface the data. Hazard scores are best-effort estimates with forecast uncertainty. Children's safety decisions rest with the operating school or government, not this platform.
> [Full terms](./TERMS.md) · [Privacy](./PRIVACY.md) · [Open data license](https://creativecommons.org/licenses/by/4.0/)

Compact version (footer):
> Decision-support, not advice. Operators own all dispatch and closure decisions. [Terms](./TERMS.md) · [Privacy](./PRIVACY.md)

---

## OSS-specific disclaimer (in LICENSE + README)

For the self-host code:

> The School Climate Hub is provided under the Apache License 2.0, which includes a NO WARRANTY disclaimer. Self-hosting organisations are solely responsible for their own deployment, security, data handling, and dispatch operations. The original maintainers accept no liability for operation of self-hosted instances.

The CC BY 4.0 license already includes a similar disclaimer for the dataset.

---

## Tenant data — current posture

As of v0.1 (UNICEF VF submission, 2026-05-17), the platform ingests one category of voluntary tenant data: **monthly school-level attendance aggregates** shared by Premier DLC for the 50 pilot schools, 2023–2025.

- No student-identifying records are ingested. Each cell is a school-month mean.
- School IDs are **anonymised** by default in all public artefacts (`school_id_01..50`). Named publication requires documented PDLC consent and a corresponding flag in [`methodology-attendance.md`](./methodology-attendance.md).
- Attendance is presented as a **correlated outcome**, not as a predictor. Causation language is prohibited in product copy, AI assistant responses, and submission materials.
- Public dataset releases include only the anonymised version. The PDLC source workbook itself is not republished; only its SHA-256 is recorded for reproducibility.

This posture supersedes the earlier "no tenant data in v0.1" stance from REQUIREMENTS §5, narrowly and only for school-level aggregates with explicit partner consent.

---

## What we promise (the positive side)

Disclaimers are necessary but not the whole story. Things we DO commit to:

- **Privacy by architecture.** We don't hold parent contacts from operators. We don't sell or share subscriber data. Ever.
- **Transparency.** Methodology, schema, scoring code, and ingestion pipelines are all open source. Anyone can audit how a score is computed.
- **Reasonable security.** Industry-standard encryption, access controls, incident response, breach notification.
- **Annual independent audit** (target — once we have funding for it): SOC 2 Type II, penetration test, ethical review.
- **Open governance** (long-term): once stewardship moves to a foundation, governance is multi-stakeholder (operators, child-health experts, technical advisors).
- **Right to fork.** If we ever pivot away from the mission, the OSS code can be forked by anyone and run by anyone.

---

## Open questions

| Q | Owner | Needed by |
|---|---|---|
| Final legal entity holding the platform (BT subsidiary / new foundation / existing partner) | Reza + Erum | Before v0.2 SaaS launch |
| Counsel engagement for TOS/Privacy drafting | Reza | Before v0.2 SaaS launch |
| Insurance: tech E&O + cyber liability policy | Reza | Before v0.2 SaaS launch |
| Jurisdiction & dispute-resolution venue | With counsel | Before v0.2 SaaS launch |
| Whether to require operators to carry their own insurance | With counsel | Before v0.2 SaaS launch |
| Ethics review board composition (for tenant-data use, especially health-incident data) | Reza + Erum + UNICEF country office contacts | Before tenant data ingestion begins |
