"""Generate the BT-branded UNICEF Venture Fund 2026 submission brief for Zeeshan.

Output: ~/Repo/school-climate-hub/docs/UNICEF-VF-Submission-Brief-Zeeshan-260515v1.docx

Uses the canonical BT styling helpers in ~/Claude/contract_styles.py
(BT_BLUE accent, Calibri, BT logo header, footer with PAGE/NUMPAGES fields).
"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/rezamalik/Claude")
from contract_styles import (
    create_doc, add_title, add_subtitle, add_heading1, add_heading2,
    add_body, add_body_bold, add_bullet, add_table, add_logo_header,
    add_footer, add_page_break, add_horizontal_line,
)

OUT = Path.home() / (
    "Library/CloudStorage/GoogleDrive-reza@beaconhouse.tech/My Drive/_Claude/"
    "Eng/PDLC/UNICEF-VF-Submission-Brief-260515v1.1.docx"
)


def placeholder(doc, label, hint=None, multiline=False):
    """Render a labelled answer slot for Zeeshan to fill."""
    add_body_bold(doc, label)
    if hint:
        p = doc.add_paragraph()
        run = p.add_run(hint)
        run.italic = True
        from docx.shared import Pt, RGBColor
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        run.font.name = "Calibri"
    add_body(doc, "[ Answer: ___________________________________________________________ ]")
    if multiline:
        add_body(doc, "[ ________________________________________________________________ ]")
        add_body(doc, "[ ________________________________________________________________ ]")


def build():
    doc = create_doc()
    add_logo_header(doc)
    add_footer(doc)

    # ---- Cover ----
    add_title(doc, "UNICEF Venture Fund 2026 — Climate Tech")
    add_subtitle(doc, "Submission Brief")
    add_body(doc, "Form: https://form.jotform.com/260711626703351")
    add_body(doc, "Deadline: 17 May 2026, 23:59 CET  ·  Funding: up to US$100,000 equity-free")
    add_body(doc, "Drafter: Zeeshan  ·  Final reviewer: Reza Malik")
    add_body(doc, "Applicant: Premier DLC (Pakistan, primary)  ·  Technical implementor: Beaconhouse Technology (Pvt) Ltd (secondary)")
    add_body(doc, "Live demo: https://schoolclimatehub.org   ·   Repo: https://github.com/school-climate-hub/school-climate-hub")
    add_horizontal_line(doc)
    add_body(doc, "How to use this document:")
    add_bullet(doc, "Sections mirror the Jotform fields in order.")
    add_bullet(doc, "Pre-filled answers are best-effort defaults — replace or refine.")
    add_bullet(doc, "Empty [ Answer: ___ ] slots need Zeeshan + Reza input. Character limits noted in red where strict.")
    add_bullet(doc, "Once finished, paste each answer into the Jotform. Don't submit from this doc.")

    add_page_break(doc)

    # ---- Section 1: Referral ----
    add_heading1(doc, "Section 1 · Referral Source")

    add_heading2(doc, "Q1.1 — How did you hear from us?")
    add_body(doc, "Dropdown options: UNICEF Website · UNICEF Venture Fund team member · Newsletter · UNICEF Country Office · Cambridge ISL · India Health Fund · LinkedIn · Facebook/Instagram · Online Search · Incubator/accelerator · AfriLabs")
    placeholder(doc, "Selection:", "(needs Reza confirm — likely 'UNICEF Country Office' if PDLC/Erum sourced via UNICEF Pakistan, else 'Online Search')")

    add_heading2(doc, "Q1.2 — Name of incubator / accelerator / Country Office / VF team member that referred you")
    placeholder(doc, "Answer:", "Conditional on Q1.1. Provide name + role if a person; provide office name if institutional.")

    add_page_break(doc)

    # ---- Section 2: Eligibility ----
    add_heading1(doc, "Section 2 · Eligibility")

    add_heading2(doc, "Q2.1 — Is your company registered as a private for-profit company?")
    placeholder(doc, "Answer (Yes/No):", "Applicant entity is Premier DLC. Confirm PDLC's SECP registration type (private for-profit Pvt Ltd vs other). If Pvt Ltd → Yes.")

    add_heading2(doc, "Q2.2 — Is your solution Open Source?")
    add_body_bold(doc, "Answer: Yes")
    add_body(doc, "Source: github.com/school-climate-hub/school-climate-hub — Apache-2.0 (repo operated by BT as technical implementor; PDLC has co-ownership of the deployment).")

    add_heading2(doc, "Q2.3 — In which country is your company legally registered?")
    add_body_bold(doc, "Answer: Pakistan")

    add_page_break(doc)

    # ---- Section 3: DEI ----
    add_heading1(doc, "Section 3 · Diversity, Equity and Inclusion")

    add_heading2(doc, "Q3.1 — Is your company founded or co-founded by women?")
    add_body_bold(doc, "Likely Answer: Yes")
    add_body(doc, "Premier DLC: confirm whether Erum (or another woman) is a named co-founder of PDLC at the corporate registration level. If yes → Yes for the applicant entity.")
    add_body(doc, "Technical implementor BT also has a woman-led C-suite (CEO Amina Kasuri, COO Fatima Kasuri) — reinforces the woman-leadership posture across the joint team.")

    add_heading2(doc, "Q3.2 — Names of woman founders / co-founders (applicant entity)")
    placeholder(doc, "Names:", "PDLC women founders/co-founders. If Erum is not technically a registered founder, name PDLC's actual women founders here.")

    add_heading2(doc, "Q3.3 — Is your company founded or led by youth (younger than 35)?")
    placeholder(doc, "Answer (Yes/No):", "Depends on PDLC leadership DOBs. Provide PDLC founders' birth years.")

    add_heading2(doc, "Q3.4 — Names of young leaders (if applicable)")
    placeholder(doc, "Names:")

    add_heading2(doc, "Q3.5 — Team table (up to 5 rows)")
    add_body(doc, "Fields per row: Full name · Position · Year of birth · Nationality · Gender · Short bio (1–2 sentences). Mix of PDLC (applicant) and BT (technical implementor) leadership — replace placeholders as needed:")
    add_table(
        doc,
        ["Full name", "Position", "Year of birth", "Nationality", "Gender", "Short bio"],
        [
            ["Erum [Surname]", "Head, Premier DLC (Applicant lead)", "____", "Pakistani", "Woman", "Leads Premier DLC's deployment of School Climate Hub across 50 PSSP/PSRP schools in Gujranwala."],
            ["Amina Kasuri", "CEO, Beaconhouse Technology (Technical implementor)", "____", "Pakistani", "Woman", "CEO of the technical implementor; oversees BT's engineering of the School Climate Hub platform."],
            ["Fatima Kasuri", "COO, Beaconhouse Technology (Technical implementor)", "____", "Pakistani", "Woman", "COO of BT; runs operations across the BT engineering portfolio."],
            ["Reza Malik", "Director, Beaconhouse Technology", "____", "Pakistani", "Man", "Director at BT; product + engineering lead for School Climate Hub."],
            ["[PDLC ops / BT engineer]", "[Position]", "____", "____", "____", "[Bio]"],
        ],
    )
    add_body(doc, "Note: roster must reflect the *applicant entity*. If UNICEF treats the team table as applicant-only, fill all 5 rows with PDLC people and move BT names to the partners section (Q5.10). If the form accepts joint-team rosters, this mix works as-is. Confirm before submit.")

    add_page_break(doc)

    # ---- Section 4: Company Information ----
    add_heading1(doc, "Section 4 · Company Information")

    add_heading2(doc, "Q4.1 — Name of company")
    placeholder(doc, "Answer:", "Premier DLC's full legal registered name (Pvt Ltd if applicable). Confirm with Erum / PDLC company secretary.")

    add_heading2(doc, "Q4.2 — Company's web page")
    placeholder(doc, "Answer:", "Premier DLC's corporate website. The School Climate Hub product site (schoolclimatehub.org) can be a secondary reference in the proposal text but the form field is the applicant company's web page.")

    add_heading2(doc, "Q4.3 — Contact person")
    placeholder(doc, "Name:", "Primary PDLC contact (likely Erum or a PDLC company-secretary-level signer).")
    placeholder(doc, "Designation:")

    add_heading2(doc, "Q4.4 — Primary e-mail address")
    placeholder(doc, "Answer:", "PDLC primary contact email (must be a domain UNICEF can verify as PDLC's).")

    add_heading2(doc, "Q4.5 — Alternate contact person email (optional)")
    add_body_bold(doc, "Suggested: reza@beaconhouse.tech")
    add_body(doc, "Reza as BT technical lead — convenient escalation for any engineering-side questions UNICEF raises during due diligence.")

    add_heading2(doc, "Q4.6 — Year company was founded")
    placeholder(doc, "Answer:", "Premier DLC's founding year — confirm with PDLC records.")

    add_page_break(doc)

    # ---- Section 5: Proposal ----
    add_heading1(doc, "Section 5 · Proposal for Raising Funds")
    add_body(doc, "Character limits in this section are strict. Word counts shown alongside each draft.")

    add_heading2(doc, "Q5.1 — Which challenges does your solution address? (multi-select)")
    add_body_bold(doc, "Tick: Area 1 (Resilient infrastructure)  +  Area 2 (Early warning, Early Action systems)")
    add_body(doc, "Skip Area 3 (Health Care readiness) and Area 4 (Point-of-Care low-connectivity) — they dilute the pitch.")

    add_heading2(doc, "Q5.2 — What need / challenge is your solution addressing locally? (max 150 chars)")
    add_body_bold(doc, "Draft (150 chars):")
    add_body(doc, "“Pakistan schools face heat, flood and AQ shocks with no per-school risk visibility. Operators react instead of pre-empt; children lose school days.”")
    placeholder(doc, "Zeeshan's version:", "Edit if a stronger phrasing exists; stay <= 150 chars.")

    add_heading2(doc, "Q5.3 — Describe your proposed solution and how it addresses the challenges (max 250 chars)")
    add_body_bold(doc, "Draft (~248 chars):")
    add_body(doc, "“An open data + AI hub giving every school real-time hazard scores, 15-day ECMWF forecasts and one-click parent advisories. Operators get evidence; families get push alerts. Pilot live across 50 PDLC schools in Gujranwala, scale to UNICEF country offices.”")
    placeholder(doc, "Zeeshan's version:", "Stay <= 250 chars.")

    add_heading2(doc, "Q5.4 — Which technology(ies) are you using?")
    add_body_bold(doc, "Tick: AI / Data Science")
    add_body_bold(doc, "Other (clarify): Open climate data ingestion (ECMWF HRES + ENS, ERA5, MODIS)")

    add_heading2(doc, "Q5.5 — How are you using the technologies? (max 150 chars)")
    add_body_bold(doc, "Draft (~140 chars):")
    add_body(doc, "“Claude 4.5 grounds answers in per-school open data; ECMWF ENS adds 15-day probabilistic forecasts; PWA delivers free parent push alerts.”")
    placeholder(doc, "Zeeshan's version:")

    add_heading2(doc, "Q5.6 — Current technical status / what's needed for pilot (max 150 chars)")
    add_body_bold(doc, "Draft (~145 chars):")
    add_body(doc, "“Live prototype: 50 schools, real ECMWF + ERA5 + MODIS data, streaming AI chat. Needed: auth, push alerts, multilingual UI, ops training.”")
    placeholder(doc, "Zeeshan's version:")

    add_heading2(doc, "Q5.7 — Results of prototyping and testing (max 150 chars)")
    add_body_bold(doc, "Draft (~150 chars):")
    add_body(doc, "“50-school dashboard live at schoolclimatehub.org. ECMWF flags a red heatwave 18–22 May; AI surfaces top-priority schools and drafts advisories.”")
    placeholder(doc, "Zeeshan's version:")

    add_heading2(doc, "Q5.8 — GitHub or other open repository link")
    add_body_bold(doc, "Answer: https://github.com/school-climate-hub/school-climate-hub")
    add_body(doc, "Public, Apache-2.0. No access grants required for @unicefinnovation.")

    add_heading2(doc, "Q5.9 — Project targets / milestones for the next 12 months (max 250 chars)")
    add_body_bold(doc, "Draft (~248 chars):")
    add_body(doc, "“3 mo: v0.2 (auth, PWA push, 4 languages, alert dispatch) — production at Gujranwala-50. 6 mo: 500-school onboarding via 1 UNICEF country office. 9 mo: 5k schools, district admin tooling. 12 mo: open API consumed by external partners; 10k+ subscribers.”")
    placeholder(doc, "Zeeshan's version:")

    add_heading2(doc, "Q5.10 — Key partners and advisors (max 150 chars)")
    add_body_bold(doc, "Draft (~145 chars):")
    add_body(doc, "“Beaconhouse Technology (technical implementor, woman-led, Pakistan); ECMWF / Copernicus / NASA Earthdata (data); Anthropic (AI).”")
    placeholder(doc, "Zeeshan's version:", "Add UNICEF Pakistan Country Office if formally engaged.")

    add_heading2(doc, "Q5.11 — How much are you seeking to raise?")
    add_body_bold(doc, "Answer: US$100,000")

    add_heading2(doc, "Q5.12 — What was your company's revenue last year?")
    placeholder(doc, "Answer (USD):", "Required field — Premier DLC 2025 revenue in USD. Confirm with PDLC finance.")

    add_heading2(doc, "Q5.13 — Overview of capital and other contributions (max 150 chars)")
    add_body_bold(doc, "Draft (~148 chars):")
    add_body(doc, "“In-kind: PDLC (school access, EMIS roster, ops). BT-funded engineering to date (technical implementor). No external grants on this project yet.”")
    placeholder(doc, "Zeeshan's version:")

    add_heading2(doc, "Q5.14 — Share application with partners?")
    add_body_bold(doc, "Answer: Yes")

    add_heading2(doc, "Q5.15 — Subscribe to UNICEF Venture Fund newsletter?")
    add_body_bold(doc, "Answer: Yes")

    add_page_break(doc)

    # ---- Section 6: Pitch Video ----
    add_heading1(doc, "Section 6 · Pitch Video")
    add_body(doc, "Spec: 2 minutes, English (or English subtitles), demo-first, uploaded to YouTube (unlisted is fine).")

    add_heading2(doc, "Suggested 2-minute script outline")
    add_table(
        doc,
        ["Time", "Beat"],
        [
            ["0:00–0:15", "Hook: “Climate makes Pakistan's school year unpredictable. 50 schools, 31k children, no per-school visibility.”"],
            ["0:15–0:35", "Solution: live dashboard at schoolclimatehub.org — show the map, click a red school."],
            ["0:35–1:00", "Forecast story: ECMWF predicts a red heatwave 18–22 May. Show the sparkline + the AI response."],
            ["1:00–1:25", "Operator workflow: open Schools list, click ‘Send advisory’, AI drafts EN/UR, operator approves."],
            ["1:25–1:45", "Open data + open source: 50 schools' data is public, Apache-2.0 repo."],
            ["1:45–2:00", "Roadmap: free push alerts via PWA, scale via UNICEF country offices, ask: $100k to v0.2."],
        ],
        col_widths=[1.0, 5.5],
    )

    add_heading2(doc, "Five video production decisions (Reza + Zeeshan to agree before recording)")
    add_bullet(doc, "1. Voiceover: Reza vs Zeeshan vs AI-generated?")
    add_bullet(doc, "2. Format: screen-capture demo only vs talking-head + demo?")
    add_bullet(doc, "3. Subtitles: burned-in vs YouTube auto-captions?")
    add_bullet(doc, "4. Music: yes / no / what?")
    add_bullet(doc, "5. Outro: contact card / partner logos / both?")

    add_heading2(doc, "Q6.1 — Upload video pitch to YouTube (link)")
    placeholder(doc, "YouTube URL:", "Test the link in an incognito window before pasting.")

    add_page_break(doc)

    # ---- Open items / blockers ----
    add_heading1(doc, "Open Items — Need PDLC + BT Sign-Off Before Submit")
    add_table(
        doc,
        ["#", "Item", "Owner", "Blocker?"],
        [
            ["1", "PDLC full legal name + registered form (Pvt Ltd / other)", "Erum / PDLC co.sec.", "YES"],
            ["2", "PDLC SECP/CR registration type — confirms for-profit eligibility (Q2.1)", "PDLC", "YES"],
            ["3", "PDLC primary contact for the form (name, designation, email)", "Erum", "YES"],
            ["4", "PDLC corporate web page URL", "Erum", "YES"],
            ["5", "PDLC women founders / co-founders for Q3.1–3.2", "Erum", "YES"],
            ["6", "DOBs of PDLC + BT team-roster members (for Q3.3 youth + Q3.5 table)", "Erum + Reza", "YES"],
            ["7", "Confirm Q3.5 roster style — applicant-only or joint applicant + implementor?", "Reza decides; cross-check Jotform hints", "YES"],
            ["8", "PDLC founding year (Q4.6)", "PDLC", "YES"],
            ["9", "PDLC 2025 revenue in USD (Q5.12)", "PDLC finance", "YES"],
            ["10", "Referral source (UNICEF CO vs Online Search)", "Erum + Reza", "No"],
            ["11", "Lock proposal copy (all 150/250-char fields)", "Zeeshan → Reza + Erum", "YES"],
            ["12", "Produce 2-minute pitch video + upload to YouTube", "Zeeshan + Reza decisions", "YES"],
            ["13", "Verify https://schoolclimatehub.org loads on HTTPS apex", "auto (Pages cert)", "No"],
            ["14", "Polish GitHub README hero / quick-start", "BT", "No"],
            ["15", "Submit before 17 May 23:59 CET (aim 16 May EOD PKT)", "PDLC submits; Reza reviews", "YES"],
        ],
        col_widths=[0.4, 3.7, 1.7, 0.8],
    )

    add_heading1(doc, "Submission Strategy")
    add_bullet(doc, "Submit by end of 16 May (PKT) to leave one full day for fixes if Jotform rejects anything.")
    add_bullet(doc, "Keep all character counts at ≤95% of the limit — leaves room for last-minute word swaps.")
    add_bullet(doc, "Upload the pitch video as unlisted on YouTube with burned-in English subtitles.")
    add_bullet(doc, "Polish the GitHub README: hero image, quick-start, link to live demo, link to docs/v0.2-scope.md.")
    add_bullet(doc, "Lead with “Pakistan-registered Pvt Ltd” wherever relevant — UNICEF programme-country status is a strength.")

    add_heading1(doc, "Credibility Talking Points (for any free-text overflow)")
    add_bullet(doc, "Working prototype with real data — schoolclimatehub.org is live, 50 schools, real ECMWF + ERA5 + MODIS, AI grounded in the dataset.")
    add_bullet(doc, "Open source from day 1 — Apache-2.0; UNICEF can fork, modify, redeploy without us.")
    add_bullet(doc, "Open data from day 1 — per-school scores, exposure timeseries and forecasts published as JSON/CSV/Parquet.")
    add_bullet(doc, "Free at point of use — public can subscribe to alerts via PWA web push; no app store, no payment, no account required.")
    add_bullet(doc, "Run cost under $20/month at pilot scale — sustainable without ongoing UNICEF subsidy.")
    add_bullet(doc, "Real deployment partner (PDLC) with EMIS roster access, not a letter of intent.")
    add_bullet(doc, "Designed for UNICEF country office adoption — multilingual (EN/UR/AR/FR planned), multi-tenant by district, no vendor lock-in.")

    doc.save(OUT)
    print(f"wrote {OUT}")
    print(f"  size: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
