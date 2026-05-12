# Access control & PII

How we keep children's-health data safe across thousands of operators, regulators, and parents.

**Principles:**
1. **Architecture beats policy.** Privacy enforced in the schema, not in promises.
2. **Need-to-know.** Every access scope-limited; every read audit-logged.
3. **Operators keep their PII.** We never ingest parent contacts.
4. **Tenants opt in to data sharing.** Nothing flows cross-tenant without explicit consent.
5. **Public good is public.** Aggregated, anonymised scores are free for anyone, anywhere.

---

## PII categories

| Category | Sensitivity | Where it lives |
|---|---|---|
| **Parent contacts** (phone, email, WhatsApp ID, language) | Highest | Operator's messaging gateway. Never the hub. |
| **Student data** (names, ages, IDs) | Highest | Operator's SIS. Never the hub. We accept aggregate counts only. |
| **School principal contact** | Medium | Hub (encrypted at rest); operator-controlled visibility |
| **Operator staff accounts** (name, email, role, login history) | Medium | Hub (encrypted at rest) |
| **Operator's roster of schools they operate** | Low | Hub; some public after operator opt-in |
| **Public hub-app subscribers** (phone or email + subscribed school list) | Medium | Hub (encrypted at rest); separate from operator data |
| **Audit log** (who did what, when, why) | Medium | Hub (immutable, encrypted); operator-readable for their tenant |
| **Hazard scores + exposure days** (per school, derived from public satellite data) | Public | Hub; CC BY 4.0 dataset; opt-in per-operator default to public for LMIC, opt-out default for OECD private |
| **Climate data tiles** (ERA5, MODIS, Sentinel-5P, CAMS, GloFAS) | Public | Hub cache; passthrough of public data |

---

## Role × access matrix

Scope notation: `tenant` = a single operator's data; `district` = a sub-scope an operator's user is assigned to within their tenant.

| Role | Reads | Writes | Scope |
|---|---|---|---|
| **Super-admin** (platform team) | System health · billing metadata · audit-log existence (not contents) | Platform config · tenant lifecycle | Platform-wide |
| **Tenant admin** (operator CEO/director) | All tenant data · audit log contents · billing | User management · roster · settings · all dispatches | Their tenant |
| **Tenant dispatcher** | Schools in assigned districts · hazard scores · drafted advisories · dispatch history | Drafts · approve & dispatch · school-day modifications | Assigned districts within tenant |
| **Tenant viewer** | Same as dispatcher, read-only | — | Assigned districts within tenant |
| **School principal** | Own school's score + dispatch log + audit confirmations | Acknowledge dispatches · report actions taken | Single school |
| **Parent / subscriber** | Subscribed schools' public scores + alerts received + own subscription profile | Subscribe / unsubscribe · channel preferences · language | Own account |
| **Researcher / public API** | Aggregated scores (k-anonymised ≥5 schools per result) · methodology · datasets | — | Whole platform, aggregated only |
| **Read-only API key (for operator dashboards)** | Same as tenant viewer | — | Per-tenant, scoped by key |

---

## Technical enforcement

### Database isolation
- **Postgres row-level security (RLS).** Every table has `tenant_id`; an RLS policy makes session-tenant match mandatory for all queries.
- **Open data tables are unscoped** by design (public aggregates) but exclude any column that could re-identify.
- **Cross-tenant queries** exist only in two cases: super-admin tooling (rate-limited, audited, requires hardware-key auth) and the open data aggregation pipeline (no PII inputs).

### Encryption
- **At rest:** AES-256 (managed by cloud provider for system tables; tenant-managed keys for high-PII columns in T3 deployments)
- **In transit:** TLS 1.3 only; TLS 1.2 blocked
- **Field-level encryption** for principal contacts and operator staff PII

### Authentication
| User class | Mechanism |
|---|---|
| Super-admin (platform team) | Hardware-key WebAuthn + SSO + IP allowlist |
| Tenant operators | Google/Microsoft OIDC; magic-link fallback; SAML for T3 |
| School principals | Magic-link email (low-friction, infrequent login) |
| Parents / subscribers | Phone OTP (universal in LMIC; no email-class barrier) |
| Researchers / API | Per-tenant API key + per-key rate limits |

### Audit
- **Every PII read or write logged** with: actor, target, timestamp, justification field, IP/UA
- **Append-only table** (revoke UPDATE/DELETE permission on the audit table for everyone including super-admins)
- **Rolling 90-day export** to operator-controlled bucket for their tenant's audit data
- **Required for** GDPR Art. 30, India DPDP Sec. 11, US COPPA, UK DPA, country-specific regimes

### Data residency
- Default: EU + US dual-region; pick nearest
- T3 operators: in-country residency option (extra infra cost, custom contract)

---

## What stays out of the hub

Some data we deliberately refuse to hold:

| Data | Why we refuse |
|---|---|
| Parent contact details (from operators) | Privacy honeypot, regulatory burden, operators won't share anyway. Tenant keeps in their messaging gateway. |
| Student names or individual IDs | We accept only aggregate counts (e.g. "school X had Y students present on date Z"). Never per-student. |
| Photos / videos of children | Out of scope; would require entirely different consent + retention regime |
| Medical records | Out of scope; we collect aggregate health-event counts only, voluntarily uploaded |
| Biometrics | Never |

---

## Voluntary tenant data ingestion (opt-in)

Operators can choose to contribute data we don't otherwise have. Always opt-in. Always aggregate-only (no per-individual records). Operator retains ownership.

| Data | Why we want it | Value to the operator |
|---|---|---|
| **Daily attendance × school × date** | Trains the climate–attendance ML model dropped from v0.1 | Exclusive "your attendance vs climate" insight; model credit |
| **Closure history** | Validates threshold calibration | Operator gets calibrated thresholds tuned to their reality |
| **Health incident logs** (heat stroke, asthma, clinic visits, aggregated) | Ground truth for child-health impact | UNICEF outcome metric; helps demonstrate impact for their own funders |
| **Infrastructure inventory** (has fan/AC, water source, cooling-centre capacity, building orientation, materials) | Drastically improves score accuracy beyond satellite | School-specific risk scoring vs generic per-coordinate score |
| **Power outage logs** | Affects cooling, insulin refrigeration | Combined climate × power-outage alerting |
| **Local tree-canopy or building surveys** | Calibrates satellite-derived canopy | More accurate per-school score |

### Ingestion principles

| Rule |
|---|
| **Always opt-in.** Base product works fully without sharing anything beyond the school roster. |
| **Per-data-type opt-in.** An operator can share attendance but not health incidents. |
| **Stripped of student-level PII before ingest.** We accept aggregate counts only. Validated server-side. |
| **Operator retains ownership.** Pull-back-and-delete API; on leaving, contributions removed from training data. |
| **k-anonymity for any cross-tenant aggregate using contributed data** (k ≥ 5 schools or ≥ 25 students, whichever is more restrictive). |
| **Federated learning option (T3 premium):** model trains on the operator's data without it ever leaving their infrastructure. |
| **Acknowledgement.** Contributing operators credited in dataset publications unless they opt for anonymity. |

---

## Public data — what's free and where to get it

The Open Data Layer is the platform's public-good contribution. Free, no signup for download, citation-ready.

| Asset | License | Format | Where |
|---|---|---|---|
| Per-school hazard scores (opt-in schools only) | CC BY 4.0 | CSV / parquet | GitHub Releases · HDX · Zenodo (DOI) |
| Aggregated district / region / country scores (all schools) | CC BY 4.0 | CSV / parquet · GeoJSON | Same |
| Methodology & schema | CC BY 4.0 | Markdown | This repo (`open_data_layer/`) |
| Daily exposure metrics (long-format) | CC BY 4.0 | Parquet (partitioned by year) | GitHub Releases |
| Vulnerability scores (latest) | CC BY 4.0 | CSV | GitHub Releases |
| Query API | CC BY 4.0 (results) | JSON | `api.schoolclimatehub.org` (rate-limited; key required for >10k req/day) |

### Public access — what's NOT included

- Any data identifying individual parents, students, principals, or operator staff
- Per-school scores for opt-out operators (aggregated regional scores still include them anonymously)
- Audit logs
- Dispatch contents (only counts)
- Tenant-contributed datasets (attendance, health, etc.) before operator opt-in to public release

### k-anonymity for API aggregates

Query results that would describe fewer than 5 schools (or fewer than 25 students in education-stats endpoints) return a `k_anonymity_floor` error with the minimum granularity the query supports. This prevents re-identification via narrowing queries.
