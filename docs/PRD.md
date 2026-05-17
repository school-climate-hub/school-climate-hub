# PRD — School Climate Hub v0.2

**Status:** Draft for v0.2 sprint kickoff
**Target launch:** ~3 weeks from start (production cutover from v0.1 static-HTML to v0.2 Next.js)
**Owner:** Reza Malik (BT) · Erum Rabbani (PTSL)
**Last updated:** 2026-05-16
**Supersedes:** v0.1 PRD (UNICEF Venture Fund 2026 submission · filed 2026-05-15 by Zeeshan)

---

## 0. What v0.1 already does (live at schoolclimatehub.org)

- Operator console for 50 PSSP/PSRP schools (PTSL-managed) in Gujranwala, Pakistan
- Real climate data: ECMWF HRES (10-day deterministic) + ENS (15-day probabilistic), Copernicus ERA5 reanalysis, NASA MODIS land-surface temperature
- Measured outcome: PDLC monthly attendance 2023–2025 — currently shows **−3.7 pp** decline across the pilot 50 (≈ 93,427 lost child-school-days vs the 2023 baseline)
- AI grounding via Anthropic Claude, refusing anything it cannot ground in the dataset
- Views: Overview · Schools · School detail · Open Data · About · Settings
- **Accreditations surface**: green-school programme status (Punjab Green School / EPCCD, WWF-Pakistan, UNESCO GEP, Eco-Schools, PSSF) rendered on each school via verified-only chips on the Schools matrix and a full card with inline summaries in the school drawer. Verification pipeline (partner-attested) lands in v0.3; v0.1 ships with curated verified records only.
- Open-source: Apache-2.0 code; CC BY 4.0 dataset; per-school exposure data anonymised by default

---

## 1. Problem (v0.2 framing)

Climate disruption is materially impacting school operations in Pakistan — heatwaves, floods, smog. v0.1 surfaced the *data*; v0.2 lets PTSL **act on it** through their existing comms channels with the right approvals, audit trail, and AI assistance. We are not a comms platform; we are the governed brain that decides what to say.

---

## 2. Users (v0.2)

| User | Auth | Role(s) |
|---|---|---|
| **Public visitor** | None | Read-only browsing of dashboard + Open Data |
| **PTSL Admin** | Magic-link | Org-wide: settings, users, imports, approvals |
| **PTSL Cluster coordinator** | Magic-link | Operate within one cluster (C-1, C-2, C-3, or C-4) |
| **PTSL Dispatcher** | Magic-link | Draft advisories org-wide; cannot approve |
| **PTSL Reviewer** | Magic-link | Read-only across all data |
| **BT (Beaconhouse Technology)** | Magic-link (admin) | Platform operations, support escalation, audit oversight |

**Out of scope for v0.2:** public-subscriber accounts (no /subscribe flow); web push; email alerts; SMS/WhatsApp gateway integration. All deferred to v0.3+.

---

## 3. v0.2 product principles

1. **Generator, not transmitter.** SCH composes the multilingual advisory copy and runs the approval workflow. PTSL dispatches through their existing channels (WhatsApp / SMS / school PA).
2. **Open-source is the moat — code is forkable, partnership and deployment are not.** Apache-2.0 covers the codebase; CC BY 4.0 covers the dataset; the hosted SaaS at `schoolclimatehub.org` is a separate offering with its own ToS, Privacy, and processor obligations. **Hosted-SaaS terms must not cross-contaminate the OSS licence.**
3. **No parent PII held.** Ever. Architectural invariant enforced at the schema layer.
4. **Governance scales with blast radius.** Routine actions are low-friction; data imports, settings changes, and privilege changes require dual-control.
5. **Operator owns the decision.** SCH surfaces evidence and drafts copy; the human approves and dispatches. No autonomous closure, no autonomous broadcast.

---

## 4. Functional requirements (v0.2)

Carries forward all v0.1 FR. New + changed:

### Auth & user management
| # | Requirement |
|---|---|
| FR-N1 | Lucia magic-link auth via `auth.schoolclimatehub.org` (SPF/DKIM/DMARC); 10-min single-use token; 8h sliding session; IP-family bound (/24 v4, /48 v6) |
| FR-N2 | Four-role model: Admin / Cluster coordinator / Dispatcher / Reviewer (definitions in §6) |
| FR-N3 | Minimum 3 admins required before "Promote to admin" or "Remove admin" UI lights up; below 3, those actions queue in a 7-day cooling window |
| FR-N4 | Cannot self-approve any gated action; initiator ≠ approver(s) by `user_id` |
| FR-N5 | Suspend/demote/remove triggers session revocation in the same DB transaction |

### Advisory generation
| # | Requirement |
|---|---|
| FR-N6 | AI advisory composer drafts in EN / UR / PA; operator edits + approves |
| FR-N7 | Copy-out buttons per language; channel audit checkboxes (WhatsApp / SMS / school PA / parent meetings) |
| FR-N8 | Threshold-triggered auto-DRAFT (cron hourly): system creates pending advisory + notifies responsible cluster coordinator via in-app banner + transactional email |
| FR-N9 | Approval gates per advisory scope (single school → 1× coordinator/admin; cluster → 1×; district → 1× admin default, opt-in 2× via Settings) |

### Data import governance
| # | Requirement |
|---|---|
| FR-N10 | School roster CSV upload requires **2× admin** approval + dry-run diff preview |
| FR-N11 | Attendance batch upload requires **2× admin** OR **1× admin + SHA-256 match** against pre-registered expected source |
| FR-N12 | Pre-registering an expected-source hash is itself a 2× admin action |
| FR-N13 | All CSV imports + exports prefix fields beginning with `= + - @ \t \r` with a leading `'` (CSV-injection guard) |

### Settings governance
| # | Requirement |
|---|---|
| FR-N14 | Hazard threshold changes require **2× admin** to commit; 1× admin can preview locally |
| FR-N15 | Threshold-trigger policy changes require **2× admin** |
| FR-N16 | Channel metadata, language defaults, branding are 1× admin |
| FR-N17 | AI system-prompt overrides: server-side only in v0.2 (no operator-facing toggle) |

### Approval workflow common rules
| # | Requirement |
|---|---|
| FR-N18 | 24-hour timeout on pending approvals; auto-expire with notification to initiator |
| FR-N19 | All approval requests notify all admins via in-app banner + Resend transactional email; suspended admins skipped; per-admin digest throttle (5 min KV-backed) |
| FR-N20 | Approval payload is content-addressed (R2 + SHA-256); execute re-hashes and aborts on mismatch |
| FR-N21 | Audit log entry for every action regardless of approval gate; hash-chained (`prev_hash`, `row_hash`) for tamper-evidence |
| FR-N22 | Emergency override (single-admin): requires ≥ 40-char written reason; max 1 per admin per 24h; broadcast to all admins + BT-controlled `oversight@` mailbox; 7-day dashboard banner; **blocked for Promote/Remove admin** |

### Chat
| # | Requirement |
|---|---|
| FR-N23 | Chat is auth-gated (operator-only); 30 queries/user/day in KV |
| FR-N24 | Anthropic prompt caching via `cache_control` on the dataset prefix; ~85% input-token cost reduction |
| FR-N25 | Chat content not logged by default (metadata only: caller, latency, token counts) |

### Accreditations
| # | Requirement |
|---|---|
| FR-N26 | Only records with `state = 'verified'` render on public surfaces (Schools matrix column, Overview rail, school drawer). Operator-declared records persist in the data layer but stay hidden until partner verification. |
| FR-N27 | Verification is a partner-attested operation in v0.3 (EPCCD Punjab, WWF-Pakistan, UNESCO GEP). v0.2 ships a 2× admin "Mark verified" override with full audit-log entry + attached evidence URL. |
| FR-N28 | Drawer renders the full label, source authority, year, and inline summary per accreditation. Compact chips on the Schools matrix surface `<TYPE> · <YEAR>` with a hover tooltip carrying the same body. Tooltips are suppressed inside the school drawer (overflow-clipped); the inline card carries the body instead. |
| FR-N29 | Accreditation badge palette is colour-coded per authority and consistent across surfaces (Schools matrix, Overview rail, drawer, About explainer card). |
| FR-N30 | Accreditations are exposed in the Open Data Layer as `accreditations.csv` (verified-only); operator-declared records do **not** export until verified. |

### Data-subject rights (DSR)
| # | Requirement |
|---|---|
| FR-N26 | `/account/export` returns the calling user's data as JSON; transactional, ≤ 30s |
| FR-N27 | `/account/delete` cascades deletes from D1 + Resend suppression + revokes sessions; 30-day SLA per Privacy Policy |

---

## 5. Non-functional requirements (v0.2)

Carries forward all v0.1 NFR. Changes:

| # | Requirement |
|---|---|
| NFR-N1 | i18n: EN + UR at launch; AR + FR added within 2 weeks post-launch; human-reviewed translations only (no AI-only flips into UR/AR/FR for user-facing copy) |
| NFR-N2 | Concurrency-safe approvals: approve + execute are each atomic single-statement D1 mutations; double-approval and double-execute impossible |
| NFR-N3 | Cannot remove yourself as admin; cannot remove last admin (TOCTOU-safe at both submit and execute) |
| NFR-N4 | DSR endpoints respond ≤ 30s; 30-day deletion SLA |
| NFR-N5 | All notification emails point to `/approvals/{id}` requiring an active session — no tokenised one-click approve from email |
| NFR-N6 | Cluster reassignment is a distinct gated action, not folded into "role change" |
| NFR-N7 | Tech E&O + cyber liability insurance bound before v0.2 launch (procurement on critical path) |
| NFR-N8 | Counsel-approved Privacy + ToS + Operator Agreement live before subscriber #1 — never any user before legal |

---

## 6. Approval matrix (full)

### Data imports
| Action | Gate | Notes |
|---|---|---|
| School roster (CSV) | 2× admin + dry-run diff | Every score downstream depends on this |
| Attendance batch | 2× admin OR 1× admin with SHA-256 match | Hash-match path needs the expected source pre-registered (itself 2× admin) |
| Climate (ERA5/MODIS/ECMWF) | None — automated | Idempotent, provider-signed |

### Settings
| Action | Gate |
|---|---|
| Hazard thresholds | 2× admin to commit; 1× admin can preview |
| Threshold-trigger policy | 2× admin |
| Channel metadata | 1× admin |
| Language defaults | 1× admin |
| Org branding | 1× admin |
| AI system-prompt overrides | Server-side only in v0.2 (no UI) |

### User management
| Action | Gate |
|---|---|
| Invite new operator (non-admin role) | 1× admin |
| Change role between non-admin tiers | 1× admin |
| Promote to admin | 2× admin |
| Remove admin | 2× admin · cannot remove self · cannot remove last admin · 7-day cooling queue when admin_count < 3 |
| Remove non-admin | 1× admin |
| Suspend user | 1× admin |
| Password / session reset for another user | 1× admin |
| Reassign cluster (Cluster coordinator) | 1× admin (distinct from role change) |

### Advisory generation
| Action | Gate |
|---|---|
| Single school | 1× admin OR cluster coordinator (their cluster only) |
| Cluster broadcast | 1× admin OR cluster coordinator (their cluster only) |
| District-wide | 1× admin (default) OR opt-in 2× admin via Settings |

---

## 7. D1 schema (skeleton)

```sql
CREATE TABLE users (
  id          TEXT PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  name        TEXT,
  role        TEXT NOT NULL,                -- 'admin'|'coordinator'|'dispatcher'|'reviewer'
  cluster_id  TEXT,                          -- nullable for non-coordinator roles
  status      TEXT NOT NULL DEFAULT 'active',-- 'active'|'suspended'|'removed'
  created_at  TEXT NOT NULL,
  last_active TEXT
);

CREATE TABLE schools (
  emis_code   INTEGER PRIMARY KEY,
  name        TEXT NOT NULL,
  cluster     TEXT NOT NULL,
  tehsil      TEXT,
  students    INTEGER,
  lat         REAL,
  lon         REAL
);

CREATE TABLE advisories (
  id            TEXT PRIMARY KEY,
  scope         TEXT NOT NULL,            -- 'school'|'cluster'|'district'
  target_id     TEXT,                      -- EMIS or cluster name; null for district
  severity      TEXT NOT NULL,             -- 'info'|'amber'|'red'
  draft_en      TEXT,
  draft_ur      TEXT,
  draft_pa      TEXT,
  final_en      TEXT,
  final_ur      TEXT,
  final_pa      TEXT,
  initiator_id  TEXT NOT NULL REFERENCES users(id),
  approval_id   TEXT REFERENCES approvals(id),
  finalised_at  TEXT,
  dispatched_via TEXT,                     -- JSON: {"whatsapp":true,"sms":true,"pa":false}
  created_at    TEXT NOT NULL
);

CREATE TABLE approvals (
  id                TEXT PRIMARY KEY,
  action_type       TEXT NOT NULL,
  target_id         TEXT,
  payload_sha256    TEXT NOT NULL,
  payload_uri       TEXT NOT NULL,         -- r2://imports/{sha}.csv or kv://approvals/{id}
  initiator_id      TEXT NOT NULL REFERENCES users(id),
  required_count    INTEGER NOT NULL DEFAULT 1,
  approver_ids      TEXT NOT NULL DEFAULT '[]',
  status            TEXT NOT NULL,         -- 'pending'|'approved'|'executed'|'expired'|'cancelled'|'blocked'
  emergency         INTEGER NOT NULL DEFAULT 0,
  emergency_reason  TEXT,                   -- ≥40 chars when emergency=1
  block_reason      TEXT,
  created_at        TEXT NOT NULL,
  expires_at        TEXT NOT NULL,
  executed_at       TEXT
);

CREATE TABLE audit_log (
  id           TEXT PRIMARY KEY,
  user_id      TEXT REFERENCES users(id),
  action       TEXT NOT NULL,
  target_id    TEXT,
  payload      TEXT,
  approval_id  TEXT REFERENCES approvals(id),
  prev_hash    TEXT NOT NULL,
  row_hash     TEXT NOT NULL,
  created_at   TEXT NOT NULL
);

CREATE TABLE magic_links (
  token_hash   TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id),
  expires_at   TEXT NOT NULL,
  used_at      TEXT,
  ip_prefix    TEXT
);

CREATE TABLE session (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id),
  expires_at   TEXT NOT NULL,
  ip_prefix    TEXT
);
```

Notes: `approvals.approver_ids` mutations are single-statement using `json_insert` with a `WHERE NOT EXISTS` self-check (race-safe). Last-admin check re-runs inside the execute transaction.

---

## 8. Out of scope (v0.2)

| Surface | Why deferred |
|---|---|
| Public-subscriber accounts (`/subscribe`) | Without dispatch from SCH, subscribers gain nothing v0.1 doesn't already give them |
| Web push (VAPID, service worker, push subscription registry) | No subscriber surface ⇒ no dispatch target |
| Email alert notifications | Deliverability discipline needs a dedicated sub-domain warm-up + 2+ weeks of practice; v0.3 |
| SMS / WhatsApp gateway integration | BYOC pass-through model planned for v0.3; PTSL operates their existing channels in v0.2 |
| Threshold-trigger auto-DISPATCH | Replaced by auto-DRAFT; operator approves and copies out |
| AI system-prompt override admin UI | High-blast-radius; v0.3 lands with 2× admin + 24h cooling + WebAuthn 2FA on approver |
| Multi-tenant operator orgs (UNICEF country offices, second-region rollouts) | PTSL single-tenant in v0.2; multi-tenant in v0.4 |
| Audit-log cryptographic verification dashboard | Hash-chain stored in v0.2; verification UI is v0.3 |
| K-anonymisation for cross-tenant attendance aggregates | Multi-tenant deliverable; v0.4 |

---

## 9. v0.3+ pre-commits

| Release | Headlines |
|---|---|
| **v0.3** | Public-subscriber accounts (email + push token; no parent PII beyond own email); web push + PWA install; email alerts on `alerts.schoolclimatehub.org` (separate warmed sub-domain); WhatsApp Business API BYOC pass-through (operator's gateway, on their bill, using their sender identity); AI prompt-override admin UI with WebAuthn 2FA |
| **v0.4** | Multi-tenant — UNICEF country offices, second-region rollouts, k-anonymised cross-tenant aggregates; SMS BYOC pass-through (Twilio / MessageBird / Pakistani aggregators); audit-log verification dashboard |
| **v0.5** | Federated trust via national EMIS APIs; published academic panel-regression (climate × attendance correlation) co-authored with research partner |

---

## 10. Open-source vs hosted SaaS

| Surface | Licence | Who runs it | Who's liable |
|---|---|---|---|
| Code (`github.com/school-climate-hub/school-climate-hub`) | **Apache-2.0** with no-warranty | Anyone who forks | The fork operator |
| Per-school dataset (anonymised) | **CC BY 4.0** with attribution + no-medical-decision addendum | Anyone | Dataset publisher (us, with PTSL consent) |
| Hosted SaaS at `schoolclimatehub.org` | **Separate SaaS ToS** (no warranty pass-through from Apache-2.0) | BT operates; PTSL is the tenant in v0.2 | BT — with cyber + tech E&O insurance, and operator indemnification scoped to operator's own misuse |

**Self-host as first-class.** Any partner (UNICEF country office, ministry, NGO) can fork and run their own instance. The PRD commits us to a `docs/self-host.md` runbook and a Docker Compose target in v0.3.

---

## 11. Success criteria (v0.2)

- [ ] **Counsel-approved** Privacy Policy + Terms of Service + Operator Agreement live before any new operator account is provisioned (jurisdiction: Pakistan with England & Wales arbitration; strictest-jurisdiction draft applied globally)
- [ ] **Tech E&O + cyber liability insurance** bound — $1M aggregate, Pakistani broker
- [ ] **All Critical + Important security findings closed** (per security-engineer review of approval matrix)
- [ ] **3 PTSL admins** onboarded and self-bootstrapped via magic-link
- [ ] **First end-to-end advisory** drafted by AI, approved by PTSL admin, copied out and dispatched via WhatsApp by PTSL (recorded in audit log)
- [ ] **First red-threshold auto-draft** generated by cron, notified to a cluster coordinator, approved within 24h
- [ ] **DSR endpoints** tested end-to-end (export + delete) with synthetic operator account
- [ ] **i18n** EN + UR live; human-reviewed translations only
- [ ] **Anthropic prompt caching** verified to give ≥ 80% input-token discount on the static prefix
- [ ] **Production cutover** from v0.1 static HTML to v0.2 Next.js completed without downtime
- [ ] **Self-host runbook** drafted (`docs/self-host.md`)
- [ ] **CONTRIBUTING.md + governance posture statement** published (open-source ecosystem expectations)

---

## 12. Open questions / pending decisions

| # | Question | Owner | Needed by |
|---|---|---|---|
| Q1 | PTSL primary channel (WhatsApp / SMS / both) — informs dispatch UI defaults | Erum | Week 1 |
| Q2 | PTSL org admin name + email + 2 additional admin contacts + cluster coordinators | Erum | Week 1 |
| Q3 | Counsel engagement (4 framing points pre-agreed) | Reza | This week |
| Q4 | Insurance procurement — Pakistani broker shortlist | Reza | This week |
| Q5 | Translator commits for UR + AR + FR (human-reviewed, named individuals) | Reza + Erum | Week 2 |
| Q6 | Jurisdiction final call (recommendation: Pakistan + England & Wales arbitration) | Reza + counsel | Week 1 |
| Q7 | `oversight@` mailbox name + BT operator | Reza | Week 1 |
| Q8 | District-wide advisory approval default (1× admin or 2× admin) — Settings opt-in available either way | Erum | Week 2 |
| Q9 | Threshold-change rollback window (24h 1× admin "revert to previous"?) | Reza | Week 2 |

---

## 13. v0.2 sprint plan (high-level)

| Week | Tracks |
|---|---|
| **Week 1** | Track A: v0.1 polish (sparkline, downloads bundle, prompt caching, HTTPS-enforced, PRD + brief regen). Track B: Next.js scaffold; i18n shell (EN + UR); D1 schema + migrations; Resend domain auth on `auth.schoolclimatehub.org`; VAPID keys generated (held for v0.3) |
| **Week 2** | Lucia auth; user/role model; approval engine (atomic D1 statements; R2-backed content-addressed payloads; hash-chained audit log); chat behind auth + rate limit + prompt caching |
| **Week 3 (or 2.5)** | Threshold auto-draft cron; transactional email to operators; AI advisory composer; DSR endpoints; counsel-finalised legal docs; production cutover |

---

## 14. References

- [REQUIREMENTS.md](./REQUIREMENTS.md) — v0.1.1 build spec (functional + non-functional)
- [DISCLAIMER.md](./DISCLAIMER.md) — risk framework + legal principles + tenant data posture
- [v0.2-scope.md](./v0.2-scope.md) — earlier v0.2 scope draft (superseded in places by this PRD)
- [methodology-attendance.md](./methodology-attendance.md) — PDLC SAR ingestion + causation framing
- [architecture.md](./architecture.md) — system architecture
- [ACCESS-CONTROL.md](./ACCESS-CONTROL.md) — tier model + role × access matrix

---

*This PRD is the single source of truth for v0.2 scope. Track B build does not begin until this is signed off.*
