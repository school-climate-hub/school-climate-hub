#!/usr/bin/env python3
"""Generate docs/PRD.docx from docs/PRD.md using the BT corporate style.
   Colors / fonts / heading patterns mirror /Users/rezamalik/Claude/contract_styles.py."""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path("/Users/rezamalik/Repo/school-climate-hub")
PRD_DOCX = ROOT / "docs" / "PRD.docx"
DRIVE_COPY = Path("/Users/rezamalik/Library/CloudStorage/GoogleDrive-reza@beaconhouse.tech/My Drive/_Claude/Eng/PDLC/BT-Eng-School-Climate-Hub-PRD-260512v1.3.docx")
LOGO = Path("/Users/rezamalik/Library/CloudStorage/GoogleDrive-reza@beaconhouse.tech/My Drive/_Claude/bt-beams-logo.png")

# BT corporate palette (from contract_styles.py)
BT_BLUE = RGBColor(0x00, 0x3D, 0x6B)
BT_DARK = RGBColor(0x33, 0x33, 0x33)
BT_GRAY = RGBColor(0x66, 0x66, 0x66)
BT_LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
TABLE_HEADER_BG = "003D6B"
TABLE_ALT_BG = "F2F2F2"

doc = Document()

# ---- Page setup: BT standard (2.54cm all sides) ----
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ---- Default font: Calibri 10pt BT_DARK, 1.15 line spacing ----
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10)
style.font.color.rgb = BT_DARK
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

# ---- Header: BT logo, left-aligned, 3.6" ----
section = doc.sections[0]
header = section.header
header.is_linked_to_previous = False
for p in header.paragraphs:
    p.clear()
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
hp.add_run().add_picture(str(LOGO), width=Inches(3.6))
hp.paragraph_format.space_after = Pt(6)

# ---- Footer: copyright + CONFIDENTIAL + Page X of N, centered, BT_GRAY 8pt ----
footer = section.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run("© 2026 Beaconhouse Technology LLC. All Rights Reserved. | CONFIDENTIAL | Page ")
run.font.size = Pt(8); run.font.color.rgb = BT_GRAY; run.font.name = 'Calibri'
# PAGE field (X)
fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE')
fr = OxmlElement('w:r'); ft = OxmlElement('w:t'); ft.text = "1"
fr.append(ft); fld.append(fr); fp._p.append(fld)
# " of "
of_run = fp.add_run(" of ")
of_run.font.size = Pt(8); of_run.font.color.rgb = BT_GRAY; of_run.font.name = 'Calibri'
# NUMPAGES field (N)
fld2 = OxmlElement('w:fldSimple'); fld2.set(qn('w:instr'), 'NUMPAGES')
fr2 = OxmlElement('w:r'); ft2 = OxmlElement('w:t'); ft2.text = "1"
fr2.append(ft2); fld2.append(fr2); fp._p.append(fld2)
for r in fp.runs:
    r.font.size = Pt(8); r.font.color.rgb = BT_GRAY; r.font.name = 'Calibri'

# ---- BT style helpers (inlined for repo self-containment) ----

def add_title(text):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.font.size = Pt(16); r.font.bold = True
    r.font.color.rgb = BT_BLUE; r.font.name = 'Calibri'
    p.paragraph_format.space_after = Pt(4)
    return p

def add_subtitle(text):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = BT_BLUE; r.font.name = 'Calibri'
    p.paragraph_format.space_after = Pt(12)
    return p

def add_heading1(text):
    p = doc.add_paragraph()
    r = p.add_run(text); r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = BT_BLUE; r.font.name = 'Calibri'
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1'); bottom.set(qn('w:color'), '003D6B')
    pBdr.append(bottom); pPr.append(pBdr)
    return p

def add_body(text, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text); r.font.size = Pt(10); r.font.name = 'Calibri'
    r.font.color.rgb = BT_DARK
    if italic: r.italic = True
    p.paragraph_format.space_after = Pt(6)
    return p

def add_bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(text); r.font.size = Pt(10); r.font.name = 'Calibri'
    r.font.color.rgb = BT_DARK
    p.paragraph_format.space_after = Pt(3)
    return p

def add_meta_line(items):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, (label, value) in enumerate(items):
        if i > 0:
            r = p.add_run("   ·   ")
            r.font.size = Pt(9); r.font.color.rgb = BT_GRAY; r.font.name = 'Calibri'
        rl = p.add_run(label + ": ")
        rl.font.size = Pt(9); rl.font.color.rgb = BT_GRAY; rl.font.name = 'Calibri'
        rv = p.add_run(value)
        rv.font.size = Pt(9); rv.font.color.rgb = BT_DARK; rv.font.name = 'Calibri'; rv.bold = True
    p.paragraph_format.space_after = Pt(14)
    return p

def set_cell_shading(cell, color_hex):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color_hex); shd.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shd)

def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.autofit = False
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.size = Pt(9); r.font.bold = True; r.font.name = 'Calibri'
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cell, TABLE_HEADER_BG)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = ''
            p = cell.paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(9); r.font.name = 'Calibri'; r.font.color.rgb = BT_DARK
            if ri % 2 == 1:
                set_cell_shading(cell, TABLE_ALT_BG)
    if col_widths:
        for ri, row_obj in enumerate(table.rows):
            for ci, w in enumerate(col_widths):
                row_obj.cells[ci].width = Inches(w)
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4')
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), '999999')
        borders.append(e)
    tblPr.append(borders)
    doc.add_paragraph()
    return table

# ============================== Content ==============================

add_title("School Climate Hub")
add_subtitle("Product Requirements Document — v0.1")

add_meta_line([
    ("Status", "Draft for 2026-05-17 UNICEF Venture Fund submission"),
    ("Owner", "Reza Malik (BT) · Erum Rabbani (PDLC)"),
    ("Last updated", "2026-05-12"),
])

add_heading1("1. Problem")
add_body("School-level climate exposure data — heat, air quality, flood, rainfall — does not exist "
         "as a clean, open, EMIS-keyed dataset. Operators rely on district-level weather and intuition. "
         "The data needed to act, school by school, isn't there.")

add_heading1("2. Users")
add_table(
    ["User", "When they use it"],
    [
        ["District operator (Zeeshan @ PDLC)", "Daily — hazard triage, advisory dispatch"],
        ["District education officer", "Weekly+ — closure decisions, escalations"],
        ["School principal", "When alerted — confirms action taken"],
        ["Parent / guardian", "When alerted — acts on advisory"],
        ["UNICEF reviewer", "One-time — evaluates the submission"],
        ["Researcher / NGO / ministry", "Ad-hoc — downloads the open dataset"],
    ],
    col_widths=[2.5, 4.0],
)

add_heading1("3. Jobs to be done")
add_table(
    ["ID", "Job", "Surface"],
    [
        ["J1", "What's happening across my estate right now?", "Overview (map + KPIs)"],
        ["J2", "Which schools need a decision today?", "Overview (active alerts)"],
        ["J3", "Send a parent advisory in 3 languages", "Dispatch flow"],
        ["J4", "Modify a school day (early dismissal, water rations)", "School-day modal"],
        ["J5", "Compare schools, drill down on one", "Schools matrix → drawer"],
        ["J6", "Understand why a school's score is high", "School drawer → Why this score?"],
        ["J7", "Get the underlying open dataset", "Open Data view"],
        ["J8", "Ask a natural-language question", "Chat (⌘K / FAB)"],
        ["J9", "Tune thresholds, languages, channels, templates", "Settings"],
        ["J10", "Broadcast advisory to an entire cluster", "Overview → cluster row"],
    ],
    col_widths=[0.5, 4.0, 2.0],
)

add_heading1("4. Features (v0.1)")
add_table(
    ["Feature", "Status"],
    [
        ["50-school roster (Gujranwala-50), EMIS + lat/lon", "Done"],
        ["Daily ingest: ERA5 / MODIS LST / Sentinel-5P / CAMS / GloFAS", "Code stubbed"],
        ["Per-school hazard scoring (heat / AQ / flood / overall) 0–100", "Mock"],
        ["Child-burden estimator (students × hazard-days)", "Mock"],
        ["Active-alert detection at configurable thresholds", "Mock"],
        ["Multilingual advisory engine (EN / UR / Punjabi-Shahmukhi)", "Mock content"],
        ["Operator approval workflow before dispatch", "UI complete"],
        ["Dispatch via SMS / WhatsApp / school PA gateway", "Stubbed"],
        ["Audit log of decisions + dispatches", "Schema only"],
        ["Open Data Layer — daily refresh, CC BY 4.0", "Schema only"],
        ["Score explainability (SHAP-style feature attribution)", "Mock"],
        ["Natural-language chat (⌘K) over the data", "Scripted demo"],
        ["Theme: light / dark / system", "Done"],
        ["Cluster-level broadcast", "UI complete"],
    ],
    col_widths=[4.7, 1.8],
)

add_heading1("5. Functional requirements")
add_table(["#", "Requirement"], [
    ("FR-1",  "Display all 50 schools on a Leaflet map with hazard-coloured markers"),
    ("FR-2",  "Switch map layer: heat / air-quality / flood / overall"),
    ("FR-3",  "Filter by cluster (C-1 to C-4)"),
    ("FR-4",  "Show child-burden estimate as the hero metric on Overview"),
    ("FR-5",  "Surface active alerts (overall ≥80) ranked by severity × students-affected"),
    ("FR-6",  "Open dispatch modal showing auto-drafted EN/UR/PA advisory text"),
    ("FR-7",  "Channel selection (SMS / WhatsApp / school PA) before send"),
    ("FR-8",  "\"Modify school day\" modal with adjustment checklist"),
    ("FR-9",  "\"Defer 24h\" action that re-queues the alert tomorrow"),
    ("FR-10", "RAG matrix table: all 50 schools, sortable by any column"),
    ("FR-11", "School detail drawer: scores, exposure, explainability — opens over any view"),
    ("FR-12", "Public download of dataset (.zip) and per-table parquet/csv"),
    ("FR-13", "Configurable hazard thresholds (red/amber per hazard)"),
    ("FR-14", "Active-language toggle (EN / UR / Punjabi-Shahmukhi / Sindhi / Pashto)"),
    ("FR-15", "Editable advisory templates per hazard"),
    ("FR-16", "Chat: ⌘K + FAB; streaming responses; tool-call display; clickable citations"),
    ("FR-17", "Chat: 5 capability buckets — query, decide, explain, draft, multilingual"),
    ("FR-18", "Cluster-level actions on Overview: click row → filter map; envelope → broadcast advisory"),
], col_widths=[0.7, 5.8])

add_heading1("6. Non-functional requirements")
add_table(["#", "Requirement"], [
    ("NFR-1", "WCAG 2.2 AA; keyboard nav; visible focus rings on all interactive elements"),
    ("NFR-2", "i18n: EN / UR / Punjabi-Shahmukhi; Intl.DateTimeFormat + Intl.NumberFormat; school names translate=\"no\""),
    ("NFR-3", "Performance: LCP < 1.5s on 3G; map renders 50 markers in single frame"),
    ("NFR-4", "Theme: system default; user override persisted in localStorage"),
    ("NFR-5", "Privacy: no parent PII in the hub; messaging gateway holds contacts"),
    ("NFR-6", "Licensing: Apache-2.0 (code) · CC BY 4.0 (open dataset)"),
    ("NFR-7", "Deployment: stateless API, static front-end, cron-driven ingest"),
    ("NFR-8", "Observability: all dispatches + decisions audit-logged with operator ID"),
    ("NFR-9", "Reduced-motion: animations honour prefers-reduced-motion: reduce"),
], col_widths=[0.7, 5.8])

add_heading1("7. Out of scope (v0.1)")
for x in [
    "Climate–attendance ML model — needs PEF SIS attendance history; deferred to Phase 1 grant deliverable",
    "Live LLM-backed chat — submission ships scripted demos; real Claude tool-use built post-funding",
    "Real SMS/WhatsApp dispatch — gateway stubbed; integrated in Phase 1",
    "Sindh / KPK expansion — pending PDLC data",
    "IoT classroom sensors — procurement risk; satellite + reanalysis is enough for v0.1",
    "Autonomous school closure — system never closes a school; that is a government call",
]:
    add_bullet(x)

add_heading1("8. Open questions / pending decisions")
add_table(
    ["#", "Question", "Owner", "Needed by"],
    [
        ["Q1", "Punjabi-Shahmukhi advisory text — needs native-speaker review", "PDLC", "2026-05-15"],
        ["Q2", "Is the 50-school footprint final, or are Sindh/KPK files coming?", "Zeeshan (PDLC)", "2026-05-14"],
        ["Q3", "Will PEF attendance history be shared, or is the ML module deferred?", "Zeeshan (PDLC)", "2026-05-14"],
        ["Q4", "Green School Sindh methodology document for narrative continuity", "Zeeshan (PDLC)", "2026-05-15"],
        ["Q5", "Demo video target length and key beats", "Reza (BT)", "2026-05-15"],
        ["Q6", "Submission package PDF — who signs the cover letter?", "Erum (PDLC)", "2026-05-16"],
    ],
    col_widths=[0.5, 3.5, 1.4, 1.1],
)

add_heading1("9. Success criteria")
for x in [
    "Submission filed by 2026-05-17 by PDLC",
    "Public demo URL live by 2026-05-16",
    "Open dataset published to GitHub Releases (target HDX + Zenodo mirror post-submission)",
    "All 10 jobs-to-be-done demonstrable in the live mockup",
    "PDLC sign-off on the operator workflow + advisory text",
    "Repo has README, LICENSE, PRD, architecture doc, open-dataset schema",
]:
    add_bullet(x)

add_heading1("10. Phase roadmap")
add_table(
    ["Phase", "Window", "Deliverables"],
    [
        ["v0.1 — Submission", "now → 2026-05-17", "PDLC pilot proves the architecture; open dataset schema; this PRD; architecture, onboarding, access-control, disclaimer docs"],
        ["v0.2 — Grant Phase 1: SaaS go-live", "2026-06 → 2026-12 (if funded)", "Multi-tenant rewrite; self-service operator signup; hosted free SaaS at schoolclimatehub.org; self-host shipped as Docker Compose; live LLM chat; real SMS/WhatsApp dispatch; audit-log persistence"],
        ["v0.3 — Parent reach", "2027 H1", "Parent / student PWA; phone-OTP subscriptions; web push + SMS + WhatsApp alerts; multilingual auto-detect; opt-in tenant data ingestion (attendance, infrastructure, health incidents)"],
        ["v0.4 — Sustainability + scale", "2027 H2 → 2028", "Premium tier for OECD operators; white-label + federation for ministries; Sindh + KPK + Bangladesh + ROSA-wide rollout; first climate-attendance ML model trained on contributed data"],
        ["v0.5 — Governance handover", "2028+", "Foundation or independent non-profit; open multi-stakeholder governance; commercial sustainability via mixed grants + paid licences + donations"],
    ],
    col_widths=[1.6, 2.0, 2.9],
)

add_heading1("11. Productisation strategy & UNICEF alignment")
add_body("Dual model: open-source code + free hosted SaaS. Both first-class.")
add_table(
    ["Channel", "Who it serves", "Why"],
    [
        ["OSS self-host\n(github.com/school-climate-hub)", "Ministries needing data residency; technical operators; researchers", "Sovereignty, auditability, no vendor lock-in"],
        ["Free hosted SaaS\n(schoolclimatehub.org, v0.2+)", "The 99% of operators without staff to run their own deployment; parents and the public", "Lowers barrier to entry; captures network-effect of cross-tenant dataset; underwrites OSS development"],
    ],
    col_widths=[2.2, 2.5, 1.8],
)
add_body("This is the GitLab / Sentry / PostHog / Plausible model adapted to a children's-health public good. "
         "Code is Apache-2.0; dataset is CC BY 4.0; running infrastructure is the value-add operators pay for "
         "(or receive funded).")

# Three product surfaces
p = doc.add_paragraph()
r = p.add_run("Three product surfaces (not one)")
r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = BT_DARK; r.font.name = 'Calibri'
p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4)
for x in [
    "Operator Console (B2B/B2G) — what v0.1 builds; multi-tenant in v0.2",
    "Open Data Platform (B2D — developers, researchers, ministries) — strengthens what's there",
    "Parent app PWA (B2C, v0.3) — anyone can subscribe to any school; phone-OTP; free",
]:
    add_bullet(x)

# Onboarding etc.
p = doc.add_paragraph()
r = p.add_run("Onboarding, access control, disclaimers")
r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = BT_DARK; r.font.name = 'Calibri'
p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4)
for x in [
    "docs/ONBOARDING.md — four-tier access model (T0 public · T1 demo · T2 verified operator · T3 federated ministry); verification workflow including conflict resolution for overlapping operator claims",
    "docs/ACCESS-CONTROL.md — PII categories, role × access matrix, technical enforcement (Postgres RLS + ABAC + encryption + audit), what we deliberately refuse to hold, voluntary opt-in tenant data ingestion (attendance, infrastructure, health incidents)",
    "docs/DISCLAIMER.md — risk profile, core legal principles (\"information not advice\"; operator owns the decision; best-available accuracy), required legal documents per launch phase",
]:
    add_bullet(x)

# Privacy posture
p = doc.add_paragraph()
r = p.add_run("Privacy posture")
r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = BT_DARK; r.font.name = 'Calibri'
p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4)
for x in [
    "We never ingest parent contacts. Tenant keeps them in their existing messaging gateway; hub fires dispatch trigger; tenant fans out.",
    "Public subscribers (parent app) sign up directly. Phone-OTP, opt-in, no identity verification (\"are you a parent?\" is exclusionary + unverifiable + irrelevant — broadcast data is public).",
    "Voluntary tenant data (attendance, infrastructure, health incidents) is opt-in only, stripped of student PII before ingest, k-anonymised for cross-tenant aggregates.",
]:
    add_bullet(x)

# UNICEF alignment
p = doc.add_paragraph()
r = p.add_run("UNICEF Green Schools & global infrastructure alignment")
r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = BT_DARK; r.font.name = 'Calibri'
p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4)
add_body("The hub is designed to plug into UNICEF's active climate-and-education infrastructure:")
add_table(
    ["Initiative", "How we fit"],
    [
        ["UNICEF Regional Green School Platform (RGSP) — launched April 2026 in Central Asia; 23M children in scope",
         "Operational infrastructure-monitoring layer for the platform's school-resilience pillar. Apache-2.0 + CC BY 4.0 makes it usable by any participating ministry without vendor negotiation."],
        ["UNICEF West & Central Africa Green School Initiative",
         "Same fit; WCA has the highest heat-stress urgency globally."],
        ["UNICEF Children's Climate Risk Index (CCRI)",
         "Our school-level data refines CCRI from sub-national to per-institution granularity. Direct contribution to UNICEF's flagship measurement product."],
        ["UNICEF Pakistan CARE programme (Climate Action & Resilience in Education)",
         "PDLC pilot sits inside CARE's geographic scope; natural country-office on-ramp."],
        ["UNESCO-led Greening Education Partnership (UNICEF partner)",
         "Open-data interoperability layer for the partnership."],
    ],
    col_widths=[2.5, 4.0],
)
add_body("We do not claim formal partnership with these programmes; we claim architectural, licensing, and data alignment. "
         "As regional Green School platforms roll out (RGSP launched 3 weeks ago; ROSA next), the hub is ready to plug in immediately.",
         italic=True)

add_body("This PRD is intentionally short. Architecture details are in docs/architecture.md. "
         "Open-dataset schema is in open_data_layer/schema.md. Onboarding / access / disclaimer docs are in docs/. "
         "Live demo at https://school-climate-hub.github.io/school-climate-hub/.",
         italic=True)

doc.save(PRD_DOCX)
print(f"wrote {PRD_DOCX}")
print(f"size: {PRD_DOCX.stat().st_size:,} bytes")
# Mirror to Drive PDLC folder
import shutil
shutil.copy2(PRD_DOCX, DRIVE_COPY)
print(f"copied to {DRIVE_COPY}")
