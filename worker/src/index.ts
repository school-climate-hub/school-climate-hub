/**
 * School Climate Hub — chat Worker
 *
 * Public endpoint:  POST /api/chat
 * Body:             { messages: [{ role: 'user' | 'assistant', content: string }, ...] }
 * Response:         text/event-stream (Server-Sent Events) carrying Anthropic streaming format
 *
 * Behaviour:
 *  1. CORS preflight handled
 *  2. Per-IP rate limit (20 req/min)
 *  3. Loads latest scores.json from the public GitHub Pages site, injects into system prompt
 *  4. Calls claude-haiku-4-5 with streaming, pipes deltas back to the browser
 *  5. Tight system prompt: answer ONLY from the dataset; refuse anything else
 *
 * Secrets (set via `wrangler secret put`):
 *   ANTHROPIC_API_KEY
 */

interface Env {
  ANTHROPIC_API_KEY: string;
  RATE_LIMIT?: { limit: (opts: { key: string }) => Promise<{ success: boolean }> };
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const SCORES_URL = "https://schoolclimatehub.org/scores.json";
const ATTENDANCE_URL = "https://schoolclimatehub.org/attendance.json";
// Fallback while the custom domain is provisioning:
const SCORES_URL_FALLBACK = "https://school-climate-hub.github.io/school-climate-hub/scores.json";
const ATTENDANCE_URL_FALLBACK = "https://school-climate-hub.github.io/school-climate-hub/attendance.json";

const MODEL = "claude-haiku-4-5";
const MAX_TOKENS = 800;

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

async function loadScoresContext(): Promise<string> {
  for (const url of [SCORES_URL, SCORES_URL_FALLBACK]) {
    try {
      const r = await fetch(url, { cf: { cacheTtl: 300 } });
      if (r.ok) {
        const data = await r.json();
        return JSON.stringify(data);
      }
    } catch (_) {
      // try next URL
    }
  }
  return JSON.stringify({ schools: [], note: "scores dataset unavailable" });
}

// Attendance is a separate file; load and inject a compact digest into the
// system prompt. We do NOT include the full per-school monthly matrix —
// token-economical to ship only aggregates + per-school annual means and
// the May anomaly metric. The model can still reason about heat × attendance
// without seeing every Jan/Feb/.../Dec cell.
async function loadAttendanceDigest(): Promise<string> {
  for (const url of [ATTENDANCE_URL, ATTENDANCE_URL_FALLBACK]) {
    try {
      const r = await fetch(url, { cf: { cacheTtl: 300 } });
      if (r.ok) {
        const d = await r.json() as any;
        const digest = {
          source: d?.meta?.provider,
          retrieved_at: d?.meta?.retrieved_at,
          school_id_anonymised: d?.meta?.school_id_anonymised,
          aggregates: d?.aggregates,
          per_school_brief: Object.fromEntries(
            Object.entries(d?.schools || {}).map(([id, s]: [string, any]) => [
              id,
              {
                students: s.students,
                cluster: s.cluster,
                annual_mean: s.annual_mean,
                pp_change_2023_2025: s.pp_change_2023_2025,
                may_anomaly_2025_vs_3yr: s.may_anomaly_2025_vs_3yr,
              },
            ])
          ),
        };
        return JSON.stringify(digest);
      }
    } catch (_) {
      // try next URL
    }
  }
  return JSON.stringify({ note: "attendance dataset unavailable" });
}

function buildSystemPrompt(scoresJson: string, attendanceJson: string): string {
  return `You are the School Climate Hub assistant, helping a school operator review climate-hazard data for 50 schools in Gujranwala, Pakistan.

CURRENT DATASET — hazard scores + forecasts (refreshed periodically; treat as the only source of truth):
${scoresJson}

MEASURED ATTENDANCE — Premier DLC monthly School Attendance Report, 2023–2025 (correlated outcome, NOT a predictor; framing rules below):
${attendanceJson}

RULES:
- Answer ONLY from the two datasets above. If the user asks about anything not in those datasets (e.g. specific historical events, schools not in the list, broader policy questions), respond: "I can only answer questions about the 50 schools in the current dataset." Exception: when discussing the 2023→2025 attendance decline you may briefly acknowledge that non-climate factors (post-COVID, economic, school-management changes) also contribute, since this acknowledgement is required by the methodology and prevents false-causation claims — do not elaborate beyond a clause.
- Cite school names exactly as they appear in 'school_name'.
- Never invent numbers. If you compute something (e.g. averages, comparisons), derive it from the dataset.
- Keep answers concise (under 150 words unless asked for detail).
- For data queries (e.g. 'which schools in C-2 are hottest'), return a short ranked list with the relevant score and student count.
- For explanation queries (e.g. 'why is X high'), describe the contributing factors using the 'raw' fields (t2m_max_c for heat, precip_24h_mm_max for rainfall) and 'scores' breakdown.
- The dataset includes a 10-day forecast per school under 'forecast' (array of {date, t2m_max_c, precip_mm, heat_score, rain_score}); 'forecast_meta' at the top level names the ECMWF HRES cycle. Use these for any deterministic question about the next 10 days. Treat heat_score >= 80 as red and 50–79 as amber.
- A 15-day probabilistic outlook is under 'forecast_ens' (array of {date, t2m_p10, t2m_p50, t2m_p90, p_red}); 'ens_meta' names the ECMWF ENS cycle. p_red is the probability (0–1) that the school crosses the red heat threshold on that day. Use this for week-2 questions and any "what's the chance/likelihood/probability" phrasing. Always cite the model and date. Frame outputs honestly: "by 26 May the ensemble shows an 84% probability of crossing the red heat threshold" — not "it will be 44°C on 26 May". Beyond 15 days say you don't have forecast coverage.
- ATTENDANCE rules: the second dataset block contains Premier DLC's measured monthly attendance for 2023, 2024, 2025. 'aggregates' has the 50-school annual means and the 2023→2025 percentage-point change. 'per_school_brief' has annual_mean per year, pp_change_2023_2025, and may_anomaly_2025_vs_3yr for each school. Use attendance when the user asks about real-world impact, historical patterns, or "did the heatwave affect anything". NEVER claim climate caused an attendance change — only say "consistent with", "correlates with", or "coincides with". The 2023→2025 decline includes non-climate drivers (post-COVID, economic). Be specific with numbers and cite years. Example acceptable phrasing: "May 2023 averaged 93.6% attendance vs February's 96.8% — consistent with heatwave-driven absenteeism." If school_id_anonymised is true, refer to schools by their id (e.g. school_id_07), not by name. Beyond 2023–2025 say you don't have attendance coverage.
- For multilingual queries: respond in the same language the user wrote in (English, Urdu, or Shahmukhi Punjabi).
- If asked about advisory drafting, suggest concrete actions but make clear the operator must approve before any dispatch.
- Never give medical, legal, or operational advice as instructions — only as suggestions for the operator's consideration.

Keep your tone professional, calm, and operator-facing. You are a tool, not a personality.`;
}

async function handleChat(request: Request, env: Env): Promise<Response> {
  // Rate limit per IP (best-effort; binding is optional)
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (env.RATE_LIMIT) {
    const { success } = await env.RATE_LIMIT.limit({ key: ip });
    if (!success) {
      return new Response(
        JSON.stringify({ error: "Rate limit exceeded. Please wait a minute and try again." }),
        { status: 429, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }
  }

  let body: { messages: ChatMessage[] };
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON body" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }
  if (!Array.isArray(body.messages) || body.messages.length === 0) {
    return new Response(JSON.stringify({ error: "messages[] required" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  const [scoresJson, attendanceJson] = await Promise.all([
    loadScoresContext(),
    loadAttendanceDigest(),
  ]);
  const system = buildSystemPrompt(scoresJson, attendanceJson);

  // Call Anthropic with streaming enabled
  const anthropicResp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: MAX_TOKENS,
      system,
      messages: body.messages,
      stream: true,
      temperature: 0.2,
    }),
  });

  if (!anthropicResp.ok) {
    const errBody = await anthropicResp.text();
    return new Response(
      JSON.stringify({ error: "Upstream LLM error", status: anthropicResp.status, detail: errBody.slice(0, 500) }),
      { status: 502, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
    );
  }

  // Stream the SSE response straight through to the client
  return new Response(anthropicResp.body, {
    status: 200,
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "X-Climate-Hub-Model": MODEL,
    },
  });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ ok: true, model: MODEL }), {
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
      });
    }

    if (url.pathname === "/api/chat" && request.method === "POST") {
      return handleChat(request, env);
    }

    return new Response(
      JSON.stringify({ error: "Not found", endpoints: ["POST /api/chat", "GET /health"] }),
      { status: 404, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
    );
  },
};
