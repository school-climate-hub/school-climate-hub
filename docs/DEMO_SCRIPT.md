# Demo Video Script — School Climate Hub v0.1

**Audience:** UNICEF Venture Fund reviewers · **Target length:** 3:30 · **Format:** screen recording with voice-over, no talking heads.

**Narrative spine:** "Zeeshan starts his day. The Hub tells him what matters. He acts." Chat is the through-line.

**Tone:** Calm, operator-first, evidence-not-promises. No jargon unless we say it once to teach it.

---

## Beat-by-beat (00:00–03:30)

### 00:00–00:20 · Hook (Problem)

| Element | Detail |
|---|---|
| **On screen** | Title card: *"Pakistan's schoolchildren bear climate costs we can't yet see."* Cut to a heatmap of South Asia, zoom to Punjab, then to 50 school pins around Gujranwala. |
| **VO** | "Every year, Pakistani schoolchildren lose weeks of learning to heat, smog, and floods. The data needed to act — school by school — doesn't exist as a clean, open dataset. Today we're building it." |
| **Music** | Subtle, low. |
| **Production** | Use stock satellite imagery for opening; final pin scatter generated from `schools.json`. |

### 00:20–00:40 · What we built (in one breath)

| Element | Detail |
|---|---|
| **On screen** | Cut to landing page (`https://school-climate-hub.github.io/school-climate-hub/`). Tagline visible. Two seconds. Then cut to dashboard Overview in light mode. |
| **VO** | "The School Climate Hub turns five open satellite sources into an operational tool for school operators — and an open dataset anyone can build on. Apache-2.0 code, Creative Commons data, deployable as a free SaaS or self-hosted for sovereignty. Founding deployment: 50 schools, 12,000 children, with Premier DLC in Gujranwala." |

### 00:40–01:30 · Daily use (Zeeshan opens his console)

| Element | Detail |
|---|---|
| **On screen** | Overview view. Cursor moves to the **child-burden hero (566,598)**, pauses 1s. Pan to the **AI insight card** — read the headline. Pan to **active alerts list** — 4 red schools visible. |
| **VO** | "It's 9 a.m. Zeeshan opens his console. The headline metric — half a million child-hazard-days this year — sets the scale. The AI insight names two schools already showing exposure 14% above their peers." |
| **Action** | Click the AI insight chip *"Why hotter?"* — chat panel slides in from right. |
| **VO** | "He asks the system why." |
| **Chat shown** | Streaming response with feature attribution: industrial heat-island proximity + low tree canopy + east-facing orientation. Citation chips clickable. |

### 01:30–02:15 · The decision (operator workflow)

| Element | Detail |
|---|---|
| **Action** | Close chat (Esc). Click first red alert card on the right rail. Drawer slides in. |
| **On screen** | School drawer: GPS Kot Bhano Shah — scores, exposure days, "Why this score?" expanded. |
| **VO** | "He drills into one school. The model explains its score with feature attribution — not a black box." |
| **Action** | Close drawer. Click the **envelope button on cluster row C-1**. Cluster broadcast modal opens. |
| **On screen** | Three-language preview: English, Urdu, Punjabi-Shahmukhi. *"Auto-substituted per school at send."* Channel selector. |
| **VO** | "He drafts a heat advisory for all 13 schools in Cluster 1 — one message, three languages, dispatched via the existing WhatsApp gateway. Operator approves; system never sends autonomously." |
| **Action** | Click *Approve & dispatch*. Status pill on the alert card flips Pending → Dispatched → Acknowledged in real time. |

### 02:15–02:45 · The open data layer (the durable contribution)

| Element | Detail |
|---|---|
| **Action** | Click **Open Data** in left sidebar. |
| **On screen** | Open Data view — four dataset cards, schema previews, CC BY 4.0 badge, "Build it yourself" panel. |
| **VO** | "Every dataset we build for PDLC is published openly. EMIS-keyed, daily refresh, schema documented. Other operators — provincial ministries, NGOs, researchers — can run their own analytics on the same foundation. This is the contribution we want to scale: not our app, the underlying open dataset." |
| **Action** | Hover the download buttons. Quick cut: GitHub Releases page in a new tab. |

### 02:45–03:10 · The roadmap (dual strategy — OSS + free SaaS)

| Element | Detail |
|---|---|
| **On screen** | Simple slide: two columns side-by-side. Left: "Self-host · github.com/school-climate-hub · Apache-2.0". Right: "Free SaaS · schoolclimatehub.org · launching with funding". Underneath: parent app icon + "Anyone can subscribe to alerts for any school." |
| **VO** | "PDLC is the founding deployment. But the design is for everyone: any ministry can self-host the code for data sovereignty; every other operator gets a free hosted SaaS at schoolclimatehub.org; and in Phase 2, parents anywhere in the world can subscribe to alerts for their child's school directly. Same code, three audiences." |

### 03:10–03:30 · The fit (UNICEF alignment + ask)

| Element | Detail |
|---|---|
| **On screen** | Quick logo bar: UNICEF Green Schools (RGSP, WCA), CCRI, Pakistan CARE programme. Then final card: project name + GitHub URL + "Premier DLC × Beaconhouse Technology". |
| **VO** | "Three weeks ago UNICEF launched the Regional Green School Platform in Central Asia — 23 million children in scope. West & Central Africa has its own Green School Initiative. ROSA is next. These platforms need an operational data layer. Apache-2.0 + CC BY 4.0 means any UNICEF country office can plug us in without negotiation. We're asking UNICEF Venture Fund to fund the bridge from pilot to platform." |
| **Final 2s** | `schoolclimatehub.org` and the GitHub URL in big text. Fade. |

---

## Production plan

### Tools
- **Screen recording**: macOS QuickTime at 1920×1080. Record dashboard at desktop resolution.
- **Editing**: Descript or DaVinci Resolve. Cuts, captions, light pacing.
- **Voice-over**: Native English narrator (Reza or Zeeshan — Zeeshan adds authenticity but English fluency must be high). Record clean WAV.
- **Captions**: Burned-in English captions throughout. Optional Urdu subtitle track as separate `.vtt` file.

### Production order
1. **Lock the dashboard** by Thu 15 May — no UI changes after this point
2. **Storyboard pass** Thu evening — paper sketches of each beat
3. **Screen record raw walkthrough** Fri morning — 4–5 takes
4. **VO record** Fri afternoon — quiet room, clean mic
5. **Edit** Fri night / Sat morning — assemble + caption + pace
6. **Internal review** Sat midday — Reza + Erum sign-off
7. **Final delivery** Sat EOD — uploaded to PDLC's preferred host (YouTube unlisted + downloadable MP4)

### Shot list (numbered, in order)

1. Landing page hero (3s)
2. Overview light theme — wide shot (4s)
3. Hover child-burden hero (2s)
4. AI insight card close-up (3s)
5. Click "Why hotter?" chip → chat slide-in (1s)
6. Chat streaming response (10s — cut for pace)
7. Citation chip click → school drawer (2s)
8. Score explainability expanded (5s)
9. Cluster broadcast button click → modal (2s)
10. Trilingual preview pan (5s)
11. Approve dispatch → status flip (3s)
12. Sidebar click → Open Data (1s)
13. Open Data hero (5s)
14. Dataset cards hover (3s)
15. GitHub Releases cut (2s)
16. Roadmap slide (8s)
17. Final card (3s)

Total ≈ 62s of recorded material, paced + cut to fit the 3:30 narrative.

### What we won't show

- Settings page (boring, distracts from the operator narrative)
- Dark theme (confusing — pick one for the demo; light reads more "institutional")
- Multiple chat exchanges (one is enough; reviewers extrapolate)
- Code editor screens (not the audience)

### Captions glossary

If the term lands in VO, the burned caption should match exactly:

- "child-hazard-days" — define first time as "student-days × hazard-exposure days"
- "feature attribution" — define as "the model shows which inputs drove the score"
- "EMIS code" — leave undefined; reviewers in the education space know it

---

## Open questions for Reza

| Q | Decision needed by |
|---|---|
| Narrator: Reza, Zeeshan, or professional VO? | 2026-05-14 |
| Native English or accented English fine? (Both have argument; accent signals authenticity) | 2026-05-14 |
| Hosting: YouTube unlisted + Drive MP4, or PDLC's own video infrastructure? | 2026-05-15 |
| Final title for the on-screen card | 2026-05-15 |
| Light theme only, or do we also produce a 30s dark-theme highlight reel? | 2026-05-14 |

---

*This script is a working draft. The chat exchange shown in beats 00:40–01:30 must use one of the 5 canned demo Q&As built into the mockup (currently: top priorities, closure decision, score explanation, draft memo, Urdu query). Recommend using the "Why hotter?" prompt — it triggers feature attribution which is the most "this is real AI" beat.*
