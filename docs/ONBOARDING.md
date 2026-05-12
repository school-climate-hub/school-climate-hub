# Onboarding & Verification

How school operators, ministries, parents, and the public get access to the School Climate Hub.

**Principle:** access proportional to risk. The public sees public data without friction; anyone dispatching real advisories to real children is verified.

---

## Access tiers

| Tier | Who | What they get | Verification |
|---|---|---|---|
| **T0 · Public** | Anyone, anywhere | Aggregated hazard scores, methodology, dataset downloads, parent-app subscriptions to any school | None — fair-use rate limit only |
| **T1 · Demo operator** | Anyone who signs up | Sandbox dashboard with sample schools; no real dispatch | Email verification + accept ToS |
| **T2 · Verified operator** | Real school operators (districts, NGOs, school chains) | Full operator console; dispatch real advisories | Legal entity + school-list verification (see below) |
| **T3 · Federated operator** | Government ministries, very large districts | Same as T2 + SAML/OIDC federation, white-label, custom legal terms | Signed legal contract + ministry-level reference |

---

## T0 — Public

No signup required for browsing aggregated data or downloading the open dataset.

A lightweight account (email or phone) is needed to:
- Subscribe to alerts for specific schools (parent-app PWA)
- Save dashboard preferences
- Use the API beyond anonymous rate limits

We collect: email or phone, language preference, subscribed-school list. Nothing else. Never sold, never shared, deletable on request.

---

## T1 — Demo operator

Anyone curious about what running the hub feels like can sign up for a demo tenant in under 2 minutes.

- Email verification
- Accept Terms of Service
- Sandbox tenant provisioned with 50 sample schools (the Gujranwala-50 dataset)
- Full UI access except dispatch (which goes to a no-op endpoint that shows "would have sent" confirmation)
- Auto-expires after 30 days unless converted to T2

Purpose: lower friction for evaluators, ministry staff, researchers, journalists who want to see the product without committing.

---

## T2 — Verified operator

The tier most operators land in. Required for any real advisory dispatch.

### Application

Submitted via web form at `schoolclimatehub.org/apply`:

| Field | Notes |
|---|---|
| Legal entity name | As registered with the relevant authority |
| Country of registration | Determines applicable legal regime |
| Registration number | Government registry # (NGO commission, education board, etc.) |
| Entity type | Public school authority / NGO / private school chain / faith-based / other |
| Primary contact | Name, role/title, work email, mobile |
| Claimed schools | List of EMIS codes (or names + coords if no EMIS); up to 5,000 in one application |
| Country-specific evidence | Letter of operation from district education officer / NGO commission certificate / school registration certificates |
| Reference | One contact at a peer operator OR a recognised body (UNICEF country office, education ministry, large funder) |

### Verification workflow

```
1. AUTO-CHECK (≤ 24 hours)
   - Entity exists in country registry (programmatic check where possible;
     manual fallback for jurisdictions without API access)
   - Domain ownership of contact email (DNS TXT challenge)
   - Cross-check claimed schools against any existing claims; flag overlaps
   - Sanctions screening (OFAC, UN, EU consolidated lists)

2. HUMAN REVIEW (≤ 5 business days)
   - Document review (registration, school list evidence)
   - Reference contacted; verifies operator's claim and authority
   - 30-minute video call with primary contact:
     · Verify identity matches submitted documents
     · Confirm operational scope (which districts, how many parents reached)
     · Walk through Acceptable Use, dispatch ethics, audit obligations
   - For high-risk jurisdictions or unverifiable entities: additional steps

3. PROVISION (immediate after approval)
   - Tenant created; claimed schools assigned
   - Primary contact gets admin account
   - Admin invites team members (dispatcher / viewer / school principal roles)
   - First-90-days monitoring: any dispatch flagged for proactive review

4. ANNUAL RECERTIFICATION
   - Contact still authorised?
   - Schools still operated by this entity?
   - Any organisational changes (merger, dissolution, sale)?
   - Re-issue or revoke
```

### Conflict resolution — overlapping claims

If two operators claim the same school, **neither dispatches to that school** until resolution.

Resolution priority:
1. **Govt-recognised primary operator** (e.g., MoU with district education office) wins
2. **Operator with EMIS-registered governance** (per the national education database) wins over informal arrangements
3. **First-verified operator** wins in absence of the above, pending appeal
4. **Escalation** to district education officer; we follow their determination

Either party can appeal in writing. Decisions documented in the public dispute log (without identifying parent data).

### Removing access

Any T2 operator can be deactivated for:
- Material breach of Acceptable Use Policy
- Failure to act on a high-risk alert with no documented reason (after warning)
- Loss of legal authority to operate the claimed schools
- Sanctions designation
- Non-payment (for paid-tier operators)

Deactivation freezes dispatch immediately; data is exported on request (90-day window) and then deleted per Privacy Policy.

---

## T3 — Federated operator

For very large deployments (government ministries, multi-million-child systems):

- All T2 verification plus signed master agreement
- SAML 2.0 or OIDC federation with the ministry's IdP
- White-label option (custom domain, branding)
- Custom data residency (data hosted in country if required)
- Negotiable SLA terms
- Dedicated technical liaison from our side
- Annual security audit included

Typical timeline: 4–8 weeks from initial contact to live deployment.

---

## Parent / student subscription (T0 sub-flow)

Independent of operator onboarding. Anyone can subscribe to alerts about any school.

```
1. Open schoolclimatehub.org (or PWA install)
2. Search for schools (by name, EMIS, district, or "near me")
3. Tap "subscribe" on each school of interest
4. Verify channel:
   - Phone OTP for SMS / WhatsApp
   - Email verification for email
   - Browser-native opt-in for web push
5. Choose alert threshold (any alert / red only / red + amber)
6. Done
```

Critical design points:
- **Anyone can subscribe to any school.** We don't verify "are you a parent?" — exclusionary and unverifiable.
- **No PII beyond contact + subscription.** No location tracking. No demographic questions. No "tell us about your children."
- **Unsubscribe is one click / one keyword.** Reply STOP, click unsubscribe link, delete account in settings.
- **Data sharing limits.** We never share subscriber data with the operator. The operator never sees who individual subscribers are — only that some non-PDLC-dispatched parents are receiving public alerts about their schools.

---

## What we **don't** do

| ✗ | Why |
|---|---|
| Collect parent contacts from operators | Privacy honeypot; operator legal teams will block; we'd lose deals. Operator keeps parent contacts in their own messaging gateway and fans dispatch out from there. |
| Verify subscribers are actual parents | Unverifiable + exclusionary + the data is public anyway |
| Onboard operators without identity + entity verification | Liability — anyone could spoof an operator and dispatch fake closure advisories |
| Auto-approve T2 applications | Real human review is the friction that protects children |
| Charge for T1 demo or T0 public access | Mission-aligned; this is public-good infrastructure |

---

## Open process questions (not yet decided)

| Q | Owner |
|---|---|
| Foundation vs commercial entity holding the SaaS — affects KYC standards | Reza + Erum |
| How we verify in jurisdictions with no public registry API | Country-by-country; manual + reference network |
| Sanctions screening provider | TBD (ComplyAdvantage, Onfido, etc.) |
| Identity verification provider for video call | TBD (Persona, Veriff, in-house) |
| Dispute resolution governance — neutral panel or our call? | Probably need a neutral panel before scaling |
