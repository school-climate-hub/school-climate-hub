# School Climate Hub — chat Worker

Cloudflare Worker that proxies chat queries from the dashboard to Anthropic Claude, with the current `scores.json` injected as system context. Tight system prompt restricts answers to the dataset.

## Deploy

```bash
cd worker
npm install
wrangler login                           # one-time browser OAuth
wrangler secret put ANTHROPIC_API_KEY    # paste the sk-ant-... key
wrangler deploy                          # ships to chat.schoolclimatehub.org
```

## Test locally

```bash
wrangler dev
curl -X POST http://localhost:8787/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Which schools are hottest right now?"}]}'
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness check; returns `{ok: true, model: claude-haiku-4-5}` |
| `POST` | `/api/chat` | Body: `{messages: [...]}` → returns SSE stream from Claude |
| `OPTIONS` | `*` | CORS preflight |

## Runtime characteristics

- **Model**: `claude-haiku-4-5` (~$0.001 per query at ~500 tokens combined)
- **Rate limit**: 20 requests/minute per client IP (Cloudflare Workers binding)
- **Temperature**: 0.2 (deterministic, low hallucination)
- **Max tokens**: 800 output
- **Caching**: `scores.json` fetched fresh per request with 300s CF edge cache
- **System prompt**: refuses anything outside the 50-school dataset; mirrors the dashboard's role-based access posture

## Cost ceiling

Worst case in the UNICEF review window:
- 100 reviewers × 15 queries each = 1,500 queries
- 1,500 × ~$0.001 = **~$1.50**
- Cloudflare Workers free tier covers 100k req/day

## Observability

```bash
wrangler tail     # real-time logs
```

Cloudflare dashboard → Workers → school-climate-hub-chat → Analytics for traffic + errors.
