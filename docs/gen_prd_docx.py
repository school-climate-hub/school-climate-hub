#!/usr/bin/env python3
"""Generate docs/PRD.docx from docs/PRD.md with BT-standard header + footer."""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path("/Users/rezamalik/Repo/school-climate-hub")
PRD_MD = ROOT / "docs" / "PRD.md"
PRD_DOCX = ROOT / "docs" / "PRD.docx"
LOGO = Path("/Users/rezamalik/Library/CloudStorage/GoogleDrive-reza@beaconhouse.tech/My Drive/_Claude/bt-beams-logo.png")

INDIGO = RGBColor(0x63, 0x5B, 0xFF)
TEXT   = RGBColor(0x0A, 0x25, 0x40)
TEXT2  = RGBColor(0x42, 0x54, 0x66)
TEXT3  = RGBColor(0x69, 0x73, 0x86)
MUTED  = RGBColor(0x88, 0x98, 0xAA)

doc = Document()

# Page setup
section = doc.sections[0]
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(0.8)
section.left_margin = Inches(0.9)
section.right_margin = Inches(0.9)

# Base style — Inter-ish (Calibri is the closest universal fallback in Word)
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10.5)
style.font.color.rgb = TEXT2
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.35

# Header: BT logo, left-aligned, 3.6"
header = section.header
htbl = header.add_table(rows=1, cols=1, width=Inches(6.7))
hcell = htbl.cell(0, 0)
hp = hcell.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
hp.add_run().add_picture(str(LOGO), width=Inches(3.6))

# Footer with page numbering field
footer = section.footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
run_a = fp.add_run("© 2026 Beaconhouse Technology LLC. All Rights Reserved. | CONFIDENTIAL | Page ")
run_a.font.size = Pt(8)
run_a.font.color.rgb = MUTED
# PAGE field
fld = OxmlElement('w:fldSimple')
fld.set(qn('w:instr'), 'PAGE')
page_run = OxmlElement('w:r')
page_text = OxmlElement('w:t')
page_text.text = "1"
page_run.append(page_text)
fld.append(page_run)
fp._p.append(fld)
# Apply size/color to the PAGE field run
for r in fp.runs:
    r.font.size = Pt(8)
    r.font.color.rgb = MUTED

# ---------- Body content ----------

def add_title(text, level=1):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    if level == 0:
        r.font.size = Pt(22)
        r.font.color.rgb = TEXT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
    elif level == 1:
        r.font.size = Pt(13)
        r.font.color.rgb = INDIGO
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
    elif level == 2:
        r.font.size = Pt(11)
        r.font.color.rgb = TEXT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
    return p

def add_para(text, color=TEXT2, size=10.5, italic=False, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.color.rgb = color
    if italic: r.italic = True
    if bold: r.bold = True
    return p

def add_meta(items):
    p = doc.add_paragraph()
    for i, (label, value) in enumerate(items):
        if i > 0:
            r = p.add_run("   ·   ")
            r.font.size = Pt(9); r.font.color.rgb = TEXT3
        rl = p.add_run(label + ": ")
        rl.font.size = Pt(9); rl.font.color.rgb = TEXT3
        rv = p.add_run(value)
        rv.font.size = Pt(9); rv.font.color.rgb = TEXT
        rv.bold = True

def set_cell_bg(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)

def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.autofit = False
    if col_widths:
        for i, w in enumerate(col_widths):
            for cell in table.columns[i].cells:
                cell.width = Inches(w)
    # Header
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        set_cell_bg(cell, "F0F1FF")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = INDIGO
    # Rows
    for ri, row in enumerate(rows):
        for ci, value in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            p = cell.paragraphs[0]
            r = p.add_run(str(value))
            r.font.size = Pt(9.5)
            r.font.color.rgb = TEXT2
    return table

def add_bullet(text, color=TEXT2):
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(2)

# ---- Title block ----
add_title("PRD — School Climate Hub v0.1", level=0)
sub = doc.add_paragraph()
sr = sub.add_run("Product Requirements Document")
sr.font.size = Pt(11); sr.font.color.rgb = TEXT3
sub.paragraph_format.space_after = Pt(10)

add_meta([
    ("Status", "Draft for 2026-05-17 UNICEF Venture Fund submission"),
    ("Owner", "Reza Malik (BT) · Erum Rabbani (PDLC)"),
    ("Last updated", "2026-05-12"),
])
doc.add_paragraph()  # spacer

# 1
add_title("1. Problem", level=1)
add_para("School-level climate exposure data — heat, air quality, flood, rainfall — does not exist "
         "as a clean, open, EMIS-keyed dataset. Operators rely on district-level weather and intuition. "
         "The data needed to act, school by school, isn't there.", color=TEXT)

# 2
add_title("2. Users", level=1)
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
    col_widths=[2.5, 4.4],
)

# 3
add_title("3. Jobs to be done", level=1)
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
    col_widths=[0.5, 4.2, 2.2],
)

# 4
add_title("4. Features (v0.1)", level=1)
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
    col_widths=[5.0, 1.7],
)

# 5
add_title("5. Functional requirements", level=1)
frs = [
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
]
add_table(["#", "Requirement"], frs, col_widths=[0.7, 6.0])

# 6
add_title("6. Non-functional requirements", level=1)
nfrs = [
    ("NFR-1", "WCAG 2.2 AA; keyboard nav; visible focus rings on all interactive elements"),
    ("NFR-2", "i18n: EN / UR / Punjabi-Shahmukhi; Intl.DateTimeFormat + Intl.NumberFormat; school names translate=\"no\""),
    ("NFR-3", "Performance: LCP < 1.5s on 3G; map renders 50 markers in single frame"),
    ("NFR-4", "Theme: system default; user override persisted in localStorage"),
    ("NFR-5", "Privacy: no parent PII in the hub; messaging gateway holds contacts"),
    ("NFR-6", "Licensing: Apache-2.0 (code) · CC BY 4.0 (open dataset)"),
    ("NFR-7", "Deployment: stateless API, static front-end, cron-driven ingest"),
    ("NFR-8", "Observability: all dispatches + decisions audit-logged with operator ID"),
    ("NFR-9", "Reduced-motion: animations honour prefers-reduced-motion: reduce"),
]
add_table(["#", "Requirement"], nfrs, col_widths=[0.7, 6.0])

# 7
add_title("7. Out of scope (v0.1)", level=1)
for x in [
    "Climate–attendance ML model — needs PEF SIS attendance history; deferred to Phase 1 grant deliverable",
    "Live LLM-backed chat — submission ships scripted demos; real Claude tool-use built post-funding",
    "Real SMS/WhatsApp dispatch — gateway stubbed; integrated in Phase 1",
    "Sindh / KPK expansion — pending PDLC data",
    "IoT classroom sensors — procurement risk; satellite + reanalysis is enough for v0.1",
    "Autonomous school closure — system never closes a school; that is a government call",
]:
    add_bullet(x)

# 8
add_title("8. Open questions / pending decisions", level=1)
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
    col_widths=[0.5, 3.7, 1.4, 1.1],
)

# 9
add_title("9. Success criteria", level=1)
for x in [
    "Submission filed by 2026-05-17 by PDLC",
    "Public demo URL live by 2026-05-16",
    "Open dataset published to GitHub Releases (target HDX + Zenodo mirror post-submission)",
    "All 10 jobs-to-be-done demonstrable in the live mockup",
    "PDLC sign-off on the operator workflow + advisory text",
    "Repo has README, LICENSE, PRD, architecture doc, open-dataset schema",
]:
    add_bullet(x)

# 10
add_title("10. Phase roadmap", level=1)
add_table(
    ["Phase", "Window", "Deliverables"],
    [
        ["v0.1 — Submission", "now → 2026-05-17", "Working demo, open dataset schema, this PRD, architecture doc"],
        ["v0.2 — Grant Phase 1", "2026-06 → 2026-12 (if funded)", "Live LLM chat, real ingest pipelines daily, real SMS/WhatsApp dispatch, audit-log persistence, deployment to PDLC infrastructure"],
        ["v0.3 — Expansion", "2027", "Climate-attendance ML model, Sindh + KPK schools, multi-tenant operator support"],
    ],
    col_widths=[1.8, 2.0, 2.9],
)

# Closing note
doc.add_paragraph()
p = doc.add_paragraph()
r = p.add_run("This PRD is intentionally short. Architecture details are in docs/architecture.md. "
              "Open-dataset schema is in open_data_layer/schema.md. The live demo is at "
              "https://school-climate-hub.github.io/school-climate-hub/.")
r.font.size = Pt(9); r.font.color.rgb = TEXT3; r.italic = True

doc.save(PRD_DOCX)
print(f"wrote {PRD_DOCX}")
print(f"size: {PRD_DOCX.stat().st_size:,} bytes")
