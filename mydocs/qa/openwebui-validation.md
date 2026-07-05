# Open WebUI Bridge Validation Checklist

Manual QA for Open WebUI fallback integration. Date: __________ Operator: __________

## Prerequisites

- [ ] Platform API running
- [ ] OpenAPI bridge: `cd deploy/openapi-bridge && uvicorn bridge:app --port 8100`
- [ ] Open WebUI running
- [ ] Test JWT from `/api/v1/auth/login`

## Bridge smoke tests

```bash
curl http://localhost:8100/health
curl http://localhost:8100/tools
curl -X POST http://localhost:8100/tools/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool":"ai_chat","arguments":{"query":"How is my sleep?"}}'
```

| Check | Pass | Notes |
|-------|------|-------|
| `/health` 200 | [ ] | |
| `/tools` lists 11 tools | [ ] | |
| `ai_predict` invoke | [ ] | |
| Missing auth → 401 | [ ] | |
| Wrong tenant token → 403 on cross-tenant | [ ] | |

## Open WebUI integration

- [ ] Custom tool/function configured to `http://openapi-bridge:8100/tools/invoke`
- [ ] Bearer token passed from user session or env
- [ ] Chat response includes medical disclaimer

## PHI boundary

- [ ] Open WebUI stores only user messages + assistant text (verify DB/settings)
- [ ] No FHIR bundles or raw profile JSON cached in UI
- [ ] Platform remains source of truth for health data

## Result

- [ ] **PASS**
- [ ] **FAIL**

Blockers:
