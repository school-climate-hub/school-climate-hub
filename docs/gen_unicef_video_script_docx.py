"""Generate the BT-branded UNICEF VF pitch-video script (2-minute video).

Output: ~/Library/CloudStorage/.../_Claude/Eng/PDLC/UNICEF-VF-Video-Script-260515v1.docx

Spec from Jotform: 2 minutes, English (or English subtitles), demo-first,
upload to YouTube. Spoken-word budget at ~140 wpm ≈ 280 words for the
whole script; we leave ~5–10% breathing room so target ~250 spoken words.

Structure: 6 beats with timing, on-screen visual, voiceover text, and
B-roll / text-overlay notes.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/rezamalik/Claude")
from contract_styles import (
    create_doc, add_title, add_subtitle, add_heading1, add_heading2,
    add_body, add_body_bold, add_bullet, add_table,
    add_logo_header, add_footer, add_page_break, add_horizontal_line,
)

OUT = Path.home() / (
    "Library/CloudStorage/GoogleDrive-reza@beaconhouse.tech/My Drive/_Claude/"
    "Eng/PDLC/UNICEF-VF-Video-Script-260515v1.docx"
)


def build():
    doc = create_doc()
    add_logo_header(doc)
    add_footer(doc)

    add_title(doc, "UNICEF Venture Fund 2026 — Pitch Video Script")
    add_subtitle(doc, "School Climate Hub · 2-minute demo")
    add_body(doc, "Submission form: https://form.jotform.com/260711626703351")
    add_body(doc, "Deadline: 17 May 2026, 23:59 CET  ·  Upload target: YouTube (unlisted is fine)")
    add_body(doc, "Live demo for screen-capture: https://schoolclimatehub.org")
    add_horizontal_line(doc)
    add_body_bold(doc, "Spec")
    add_bullet(doc, "Total length: 2:00 (hard cap; UNICEF discards anything longer)")
    add_bullet(doc, "Language: English (or another language with English subtitles burned in — safer than YouTube auto-captions)")
    add_bullet(doc, "Format: demo-first — UNICEF prefers seeing the product working over talking-head intros")
    add_bullet(doc, "Spoken-word budget: ~250 words at ~140 wpm (leaves breathing room and pauses)")
    add_bullet(doc, "Aspect: 16:9, 1080p minimum, MP4")
    add_bullet(doc, "Audio: clean room sound; if narrated, monitor with headphones during recording")

    add_page_break(doc)

    # ---- The script ----
    add_heading1(doc, "Script · beat-by-beat (≈250 spoken words)")

    # Beat 1 — Hook (0:00 – 0:15)
    add_heading2(doc, "Beat 1 · Hook  (0:00 – 0:15)")
    add_body_bold(doc, "On screen:")
    add_body(doc, "Fast cuts: a Pakistani village schoolyard in heat shimmer → an empty classroom mid-school-day → a temperature reading of 42 °C on a phone. Title card overlays: “Pakistan, May 2026 · 50 schools · 31,000 children”.")
    add_body_bold(doc, "Voiceover (~30 words):")
    add_body(doc, "“Across Pakistan, climate is rewriting the school year. Heatwaves, floods, smog — every shock costs school-days. And operators today have no per-school visibility into what's coming next.”")

    # Beat 2 — Solution intro (0:15 – 0:35)
    add_heading2(doc, "Beat 2 · Solution intro  (0:15 – 0:35)")
    add_body_bold(doc, "On screen:")
    add_body(doc, "Smooth screen-capture: open https://schoolclimatehub.org. Map of Gujranwala-50 schools appears, markers coloured by today's exposure. Cursor pans, clicks a school. Side panel slides in with name, students, today's heat score, raw temperature.")
    add_body_bold(doc, "Voiceover (~35 words):")
    add_body(doc, "“This is School Climate Hub. Open data, AI-grounded, free at the point of use. For every one of 50 pilot schools we publish today's hazard exposure and a 15-day forecast — built from ECMWF, NASA, and Copernicus.”")

    # Beat 3 — Forecast story (0:35 – 1:00)
    add_heading2(doc, "Beat 3 · Forecast story  (0:35 – 1:00)")
    add_body_bold(doc, "On screen:")
    add_body(doc, "Click the school's forecast tab. Sparkline animates: HRES 10-day red line climbing through 18–22 May into the red threshold, ENS p10–p90 band widening through week 2. Caption overlay: “ECMWF HRES + ENS · issued 2026-05-13T12:00Z”.")
    add_body_bold(doc, "Voiceover (~40 words):")
    add_body(doc, "“The model is unambiguous: a red-threshold heatwave is landing on these schools 18 through 22 May, with the ensemble showing an 86% chance of red-heat days continuing into week 2. That's actionable. That's a closure decision.”")

    # Beat 4 — Operator workflow (1:00 – 1:25)
    add_heading2(doc, "Beat 4 · Operator workflow  (1:00 – 1:25)")
    add_body_bold(doc, "On screen:")
    add_body(doc, "Open “Ask the hub” chat. Type: “Should we close schools 18–22 May?” Stream Claude's response — cites HRES cycle, names the highest-burden schools, drafts an advisory. Click “Send advisory”. Modal shows EN / Urdu / Punjabi text, the operator clicks Approve. Quick cut to a parent's phone receiving a web-push notification.")
    add_body_bold(doc, "Voiceover (~45 words):")
    add_body(doc, "“The operator asks; the AI answers from the dataset — no guessing. It drafts a closure advisory in English, Urdu, or Punjabi. The operator reviews, approves, and parents receive a push notification on any phone — no app store, no SMS cost, no proprietary platform.”")

    # Beat 5 — Open & free (1:25 – 1:45)
    add_heading2(doc, "Beat 5 · Open and free  (1:25 – 1:45)")
    add_body_bold(doc, "On screen:")
    add_body(doc, "Cut to GitHub repo page — Apache-2.0 badge visible. Cut to the Open Data page on the site. Pull-quote overlay: “Per-school hazard data, published openly”. Then a clean shot of partner logos: Premier DLC, ECMWF, NASA, Anthropic.")
    add_body_bold(doc, "Voiceover (~35 words):")
    add_body(doc, "“Every line of code is Apache-2.0. Every per-school dataset is published openly. So any UNICEF country office, any district, any researcher — can fork, replicate, and extend, without us in the loop.”")

    # Beat 6 — Roadmap + ask (1:45 – 2:00)
    add_heading2(doc, "Beat 6 · Roadmap and ask  (1:45 – 2:00)")
    add_body_bold(doc, "On screen:")
    add_body(doc, "Three milestone tiles fade in: “v0.2 production — 50 schools” → “500 schools via first UNICEF country office” → “5,000 schools, district admin tooling”. End card: schoolclimatehub.org · github.com/school-climate-hub · Beaconhouse Technology + Premier DLC logos.")
    add_body_bold(doc, "Voiceover (~30 words):")
    add_body(doc, "“With UNICEF Venture Fund support, we'll harden the platform, ship it in four languages, and onboard the first country-office partner. School Climate Hub — schoolclimatehub.org.”")

    add_page_break(doc)

    # ---- Shot list ----
    add_heading1(doc, "Shot list")
    add_body(doc, "Shots in production order. Screen-capture for any cursor activity is mandatory — record at native resolution on the deployed site, not localhost.")
    add_table(
        doc,
        ["#", "Beat", "Shot", "Capture method", "Duration"],
        [
            ["1", "1 · Hook", "B-roll: school yard heat shimmer / empty classroom / phone showing 42 °C", "Stock or borrowed PDLC photo + Premiere/CapCut", "~10 s"],
            ["2", "1 · Hook", "Title card: “Pakistan · May 2026 · 50 schools · 31,000 children”", "After Effects or Keynote export", "~5 s"],
            ["3", "2 · Solution", "Open schoolclimatehub.org, map renders, zoom into Gujranwala-50, click a school", "ScreenStudio at 1080p / 30fps", "~20 s"],
            ["4", "3 · Forecast", "Open school detail, forecast sparkline animates HRES + ENS bands", "ScreenStudio + JS-driven Recharts animation on the live site", "~25 s"],
            ["5", "4 · Operator", "Open “Ask the hub”, type the closure question, stream response", "ScreenStudio at 1080p; pre-warm the chat to keep latency clean", "~15 s"],
            ["6", "4 · Operator", "Open “Send advisory” modal, show EN/UR/PA text, click Approve", "ScreenStudio + a parent-phone insert (own phone, vertical)", "~10 s"],
            ["7", "5 · Open", "GitHub repo page; Apache-2.0 badge prominent", "ScreenStudio at 1080p", "~8 s"],
            ["8", "5 · Open", "Open Data page + partner logo strip", "ScreenStudio + simple still composition", "~12 s"],
            ["9", "6 · Roadmap", "Three roadmap tiles fade in", "Keynote / After Effects", "~12 s"],
            ["10", "6 · End card", "URL + partner logos + contact", "Keynote / After Effects", "~3 s"],
        ],
        col_widths=[0.4, 1.1, 3.0, 1.8, 0.6],
    )

    add_page_break(doc)

    # ---- Five production decisions ----
    add_heading1(doc, "Five production decisions (Reza + Zeeshan to lock before recording)")
    add_table(
        doc,
        ["#", "Decision", "Options", "Recommendation"],
        [
            ["1", "Voiceover voice", "Reza · Zeeshan · AI generated (ElevenLabs-style)", "Human voice — Reza or Zeeshan — feels more credible than synthetic for a $100k pitch"],
            ["2", "Format", "Screen-capture demo only · Talking-head intro + demo · Hybrid (face PiP)", "Screen-capture demo only — UNICEF VF reviews many pitches and demo-first stands out"],
            ["3", "Subtitles", "Burned-in English subtitles · YouTube auto-captions · None", "Burned-in — auto-captions miss technical terms (ECMWF, ENS, Anthropic) and look amateur"],
            ["4", "Music", "None · Soft tech-ambient (royalty-free) · Light percussion", "Soft tech-ambient under voiceover at -22 dB; silence on the ask line at the end"],
            ["5", "End-card", "Partner logos + URL only · + contact email · + QR code to demo", "URL + partner logos + reza@beaconhouse.tech (small, bottom-right). QR is overkill for a 3-second card."],
        ],
        col_widths=[0.4, 1.6, 2.8, 2.2],
    )

    add_page_break(doc)

    # ---- Asset checklist ----
    add_heading1(doc, "Asset checklist")
    add_bullet(doc, "BT logo (PNG with transparent background) — already in repo")
    add_bullet(doc, "Premier DLC logo (request from Erum)")
    add_bullet(doc, "UNICEF Venture Fund acknowledgement style guide — confirm if logos can be shown without prior approval; if not, use neutral wording instead")
    add_bullet(doc, "Royalty-free background music — recommend YouTube Audio Library (track suggestions: “Vibing”, “Acoustic Folk Instrumental”, or similar tech-ambient)")
    add_bullet(doc, "PDLC school photo (one wide shot, used for Beat 1 B-roll) — request from Erum; ensure no identifiable children faces unless consented")
    add_bullet(doc, "Parent phone for the push-notification shot — own phone is fine; vertical orientation, light room, screen brightness high")
    add_bullet(doc, "Recording environment — quiet room, lavalier or USB-condenser mic, no echo. Test 10 seconds, listen back, then commit to the take")

    add_heading1(doc, "Production workflow (suggested)")
    add_table(
        doc,
        ["Step", "Time", "What"],
        [
            ["1", "30 min", "Pre-flight: open schoolclimatehub.org, prewarm the chat, ensure DNS + cert green, ensure scores.json is current"],
            ["2", "45 min", "Record voiceover in one take per beat (6 short clips, easier to re-record than one long one)"],
            ["3", "60 min", "Record screen-captures using ScreenStudio at 1080p / 30fps, one beat per take"],
            ["4", "20 min", "Capture B-roll on the parent phone, title cards in Keynote"],
            ["5", "90 min", "Edit in Descript or CapCut Pro: align VO + screen-capture + B-roll, burn in subtitles, mix music at -22 dB"],
            ["6", "15 min", "Export 1080p MP4, watch end-to-end with headphones, fix any audio glitches"],
            ["7", "10 min", "Upload to YouTube as unlisted, copy the URL into the Jotform"],
            ["8", "10 min", "Test the link in an incognito browser before submission"],
        ],
        col_widths=[0.5, 0.8, 5.2],
    )
    add_body(doc, "Total realistic time: ~4 hours focused, with all assets ready. Schedule one buffer day before the 17 May deadline.")

    doc.save(OUT)
    print(f"wrote {OUT}")
    print(f"  size: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
