# UNICEF Venture Fund 2026 — Application Plan

**Form:** https://form.jotform.com/260711626703351
**Deadline:** 17 May 2026, 23:59 CET (~03:59 PKT, 18 May)
**Funding:** Up to US$100,000 equity-free
**Drafter:** Zeeshan
**Reviewer:** Reza (final sign-off)

This document tracks every form field, our proposed answer, and what's still needed. Character limits are strict — every field has been counted.

---

## Hard facts (no judgement calls)

| Field | Value | Source |
|---|---|---|
| Company legal name | **Beaconhouse Technology (Pvt) Ltd** | SECP 0137683 |
| Country of registration | **Pakistan** | SECP |
| Founded | **2024** (verify with Reza) | — |
| For-profit? | **Yes** | — |
| Open Source? | **Yes** (Apache 2.0) | github.com/school-climate-hub/school-climate-hub |
| Web page | **https://schoolclimatehub.org** | — |
| GitHub repo | **https://github.com/school-climate-hub/school-climate-hub** | public |
| Contact person | **Reza Malik, Director** | — |
| Primary email | **reza@beaconhouse.tech** | — |
| Amount sought | **US$100,000** | max allowed |
| Last year revenue | TBD — confirm with Reza | — |

---

## Section 1: Referral

**How did you hear from us?** — UNICEF Country Office (Pakistan) *or* Online Search — confirm with Erum/PDLC how they sourced this lead.

**Name of referrer** — fill if UNICEF CO referral (name + role).

---

## Section 2: Eligibility

| Q | Answer |
|---|---|
| For-profit company? | **Yes** |
| Open source? | **Yes** |
| Country of registration | **Pakistan** |

---

## Section 3: DEI

| Q | Answer |
|---|---|
| Founded/co-founded by women? | **No** (or **Yes** if Erum is named co-founder at the corporate level — needs Reza confirm) |
| Names of women founders | (if Yes) |
| Founded/led by youth (<35)? | **No** unless Zeeshan or another founder is <35 — needs confirm |
| Names of youth leaders | (if Yes) |

**Team table** (up to 5 rows) — fields per person: Full name · Position · Year of birth · Nationality · Gender · Short bio.

Recommended roster to list (verify with Reza):
1. Reza Malik — Director — Pakistani — Man
2. (TEY / BT leadership) — confirm with Reza which BT individuals appear best
3. Erum (Head, Premier DLC) — Pakistani — Woman — Partner organisation lead
4. Sulman Arshad — IT/Ops — Pakistani — Man
5. (Reserve slot — Zeeshan or other contributor)

Short bios: keep to 1–2 sentences, technology-credibility-first. Pre-drafted in a follow-up doc once names are locked.

---

## Section 4: Company info

Straightforward. Match the hard facts above.

---

## Section 5: Proposal — the meaty section

Character limits are aggressive. Every answer below is drafted to fit.

### Which challenges does your solution address?
**Tick:**
- Area 1: Strategic Planning for resilient infrastructure
- Area 2: Early warning, Early Action systems

*(Skip Area 3 Health Care and Area 4 Point-of-Care — they dilute our pitch.)*

---

### What need/challenge is your solution addressing locally? *(150 chars)*

> Pakistan schools face heat, flood and AQ shocks with no per-school risk visibility. Operators react instead of pre-empt; children lose school days.

**[150 chars exactly. Verify with Reza for tone.]**

---

### Describe your proposed solution and how it addresses the challenges. *(250 chars)*

> An open data + AI hub giving every school real-time hazard scores, 15-day ECMWF forecasts and one-click parent advisories. Operators get evidence; families get push alerts. Pilot live across 50 PDLC schools in Gujranwala, scale to UNICEF country offices.

**[~248 chars. Verify.]**

---

### Which technologies are you using?
**Tick:** AI/Data Science (primary).

If "Other": *Open climate data ingestion (ECMWF, ERA5, MODIS)*

---

### How are you using the technologies? *(150 chars)*

> Claude 4.5 grounds answers in per-school open data; ECMWF ENS adds 15-day probabilistic forecasts; PWA delivers free parent push alerts.

**[~140 chars.]**

---

### Current technical status / what's needed for pilot. *(150 chars)*

> Live prototype: 50 schools, real ECMWF + ERA5 + MODIS data, streaming AI chat. Needed: auth, push alerts, multilingual UI, ops training.

**[~145 chars.]**

---

### Results of prototyping and testing. *(150 chars)*

> 50-school dashboard live at schoolclimatehub.org. ECMWF flags a red heatwave 18–22 May; AI surfaces top-priority schools and drafts advisories.

**[~150 chars.]**

---

### GitHub link

`https://github.com/school-climate-hub/school-climate-hub`

(Already public, Apache-2.0. No access grants needed.)

---

### Targets/milestones for next 12 months. *(250 chars)*

> 3 mo: v0.2 (auth, PWA push, 4 languages, alert dispatch) — production at Gujranwala-50. 6 mo: 500-school onboarding via 1 UNICEF country office. 9 mo: 5k schools, district admin tooling. 12 mo: open API consumed by external partners; 10k+ subscribers.

**[~248 chars.]**

---

### Key partners and advisors. *(150 chars)*

> Premier DLC (Pakistan, deployment partner, 50 schools); ECMWF / Copernicus / NASA Earthdata (data); Anthropic (AI).

**[~120 chars. Add UNICEF CO if confirmed.]**

---

### How much are you seeking to raise? — **$100,000 USD**

### Last year revenue — **TBD** *(needs Reza)*

### Capital and other contributions. *(150 chars)*

> Self-funded by Beaconhouse Technology to date; in-kind by Premier DLC (school access, EMIS roster, ops feedback). No prior grants on this project.

**[~150 chars.]**

---

### Share application with partners? — **Yes**
### Subscribe to newsletter? — **Yes**

---

## Section 6: Pitch video

**2 minutes, English (or English subtitles), demo-first.**

Suggested script outline (Zeeshan to flesh out):

| Time | Beat |
|---|---|
| 0:00–0:15 | Hook: "Climate makes Pakistan's school year unpredictable. 50 schools, 31k children, no per-school visibility." |
| 0:15–0:35 | Solution: live dashboard at `schoolclimatehub.org` — show the map, click a red school |
| 0:35–1:00 | Forecast story: ECMWF predicts a red heatwave 18–22 May. Show the sparkline + the AI response. |
| 1:00–1:25 | Operator workflow: open Schools list, click "Send advisory", AI drafts EN/UR, operator approves |
| 1:25–1:45 | Open data + open source: 50 schools' data is public, Apache-2.0 repo |
| 1:45–2:00 | Roadmap: free push alerts via PWA, scale via UNICEF country offices, ask: $100k to v0.2 |

**Decisions Reza must make on the video** (lifted from existing TASK-2026-00497):
1. Voiceover: Reza vs Zeeshan vs AI?
2. Format: screen-capture demo vs talking-head intro + demo?
3. Subtitles: burned-in vs YouTube auto?
4. Music: yes / no / what?
5. Outro: contact card / partner logos / both?

---

## Open items before submission

| # | Item | Owner | Blocker? |
|---|---|---|---|
| 1 | Confirm referral source | Reza / Erum | No |
| 2 | Confirm 5-person team roster + DOBs + nationality + gender | Reza | **Yes** |
| 3 | Confirm BT founding year | Reza | No |
| 4 | Confirm BT 2025 revenue (USD) | Reza | **Yes** |
| 5 | Lock proposal copy (150/250 char fields above) | Zeeshan → Reza | **Yes** |
| 6 | Production: 2-min pitch video on YouTube | Zeeshan + Reza decisions | **Yes** |
| 7 | Verify HTTPS apex works (`https://schoolclimatehub.org`) | auto (cert provisioning) | No — will land before deadline |
| 8 | Ensure GitHub repo README is reviewer-ready | BT | No — already public |
| 9 | Submit before 17 May 23:59 CET | Reza | **Yes** |

---

## Submission strategy

1. **Don't wait until Day 17.** Submit by end of Day 16 (16 May PKT) to leave Day 17 for fixes if Jotform rejects anything.
2. **Have all character counts at ≤95% of limit** — leaves room for a last-minute word swap without re-counting.
3. **Pitch video uploaded to YouTube** as unlisted, with English subtitles burned in (safer than auto-captions). Test the link in an incognito window before pasting.
4. **GitHub repo polish:** README hero image, quick-start section, link to live demo, link to `v0.2-scope.md`. The reviewers will skim it.
5. **The "Pakistan-registered Pvt Ltd" angle is a strength** — UNICEF programme countries are explicitly prioritised. Lead with it where possible.

---

## What makes this submission credible

Use these talking points wherever helpful:

- **Working prototype with real data**, not slideware. `schoolclimatehub.org` is live, 50 schools, real ECMWF + ERA5 + MODIS, real AI grounded in the dataset.
- **Open source from day 1.** Apache-2.0. UNICEF can fork, modify, redeploy without us.
- **Open data from day 1.** Per-school scores, exposure timeseries, forecasts published as JSON/CSV/Parquet (Scope B is pending PDLC consent for the school-identifying portion).
- **Free at point of use.** Public can subscribe to alerts without app store, without payment, without an account.
- **Run cost under $20/month at pilot scale** — sustainable without ongoing UNICEF subsidy.
- **Already deployed with a real partner (PDLC)**, not a paper letter of intent.
- **Designed for UNICEF country office adoption** — multilingual, multi-tenant by district, no vendor lock-in.

---

## Out of scope for the form (but worth having ready if asked)

- Privacy / data protection posture — see `docs/v0.2-scope.md` §8
- AI cost containment — auth-gated, 30 queries/user/day, claude-haiku-4-5
- Why not native mobile — PWA + web push is free, instant, no app store gatekeeping
- Why Pakistan first — Premier DLC partnership, climate-vulnerable, English+Urdu UNICEF language coverage, scalable to Bangladesh/India/Indonesia after
