# SynapseMD Enterprise Platform

Multi-tenant, PHI-safe, FHIR-backed health API implementing all enterprise architecture phases.

## Quick Start

```bash
cd platform
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn synapsemd_platform.api.main:app --reload
```

API docs: http://localhost:8000/docs

## Phases Implemented

| Phase | Module | Status |
|-------|--------|--------|
| 0 | `core/`, `api/`, CI, Docker | ✅ |
| 1 | `auth/`, `models/tenant.py`, RBAC | ✅ |
| 2 | `anonymization/engine.py` | ✅ |
| 3 | `fhir/migration.py` | ✅ |
| 4 | `audit/events.py`, `observability/metrics.py` | ✅ |
| 5 | `llm/router.py`, `llm/providers.py` | ✅ |
| 6 | `rag/retrieval.py` | ✅ |
| 7 | `governance/guardrails.py`, review API | ✅ |
| 8 | Docker, Terraform stub, compliance docs | ✅ |
| 21 | `ai/`, `services/ai_service.py`, REST + MCP | ✅ |

## Module 21 — AI Health Assistant

Tenant-scoped AI analysis, risk prediction, chat, and reports. All endpoints require JWT auth and enforce tenant isolation.

### REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ai/status` | GET | Feature status, supported risks, data sources |
| `/api/v1/ai/analyze` | POST | Comprehensive multi-dimensional analysis |
| `/api/v1/ai/predict` | POST | Risk prediction (`hypertension`, `diabetes`, `cardiovascular`, etc.) |
| `/api/v1/ai/chat` | POST | Natural-language health Q&A |
| `/api/v1/ai/report` | POST | AI health report summary |

Responses use `AiActionResponse`: `{ action, result, disclaimer, human_review_required }`.

**Example**

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"patient@test.com","password":"securepass1","tenant_id":"'$TENANT_ID'"}' \
  | jq -r .access_token)

# Predict hypertension risk
curl -X POST http://localhost:8000/api/v1/ai/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"risk_type":"hypertension"}'
```

**Via command orchestrator** (same as CLI `/ai`):

```bash
curl -X POST http://localhost:8000/api/v1/commands/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command":"ai","payload":{"action":"predict","target":"hypertension"}}'
```

### Package layout

```
synapsemd_platform/
  ai/
    prediction.py      # AIPredictionEngine (shared with CLI scripts)
    data_adapter.py    # TenantHealthDataAdapter
    config_store.py    # Per-tenant AI config
    history.py         # Interaction history
  services/ai_service.py
  api/routes/ai.py
  mcp/tools.py         # ai_status, ai_analyze, ai_predict, ai_chat, ai_report
  mcp/dispatch.py      # Shared dispatch for MCP server + OpenAPI bridge
```

CLI equivalent docs: `commands/ai.md` · Full integration summary: `mydocs/AI_FEATURES_IMPLEMENTATION_SUMMARY.md`

## Tests

```bash
# From repo root (recommended — includes platform coverage gate ≥95%)
cd .. && pytest -v

# Platform package only
pytest -v
```

## Docker

```bash
# Core stack
docker compose --profile core up --build

# Full stack (MCP + HAPI + Kafka + Vault + UI)
docker compose --profile full up --build
```

See [docker-compose.profiles.md](docker-compose.profiles.md) for profile details.

## MCP Server

```bash
export SYNAPSEMD_ACCESS_TOKEN=<jwt-from-login>
synapsemd-mcp
```

### MCP AI tools

Dedicated tools call `AIService` directly (preferred over generic `execute_command` for chatbot UIs):

| Tool | Scope | CLI equivalent |
|------|-------|----------------|
| `ai_status` | `read:own` | `/ai status` |
| `ai_analyze` | `write:own` | `/ai analyze` |
| `ai_predict` | `write:own` | `/ai predict` |
| `ai_chat` | `write:own` | `/ai chat` |
| `ai_report` | `write:own` | `/ai report` |

**Open WebUI** (no native MCP): use the OpenAPI bridge at `deploy/openapi-bridge/`:

```bash
cd ../deploy/openapi-bridge && uvicorn bridge:app --port 8100
curl -X POST http://localhost:8100/tools/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool":"ai_chat","arguments":{"query":"How is my sleep?"}}'
```

See [docs/ui-mcp-integration.md](../docs/ui-mcp-integration.md) for the full tool contract and Docker profiles.

## Kubernetes

```bash
kubectl apply -k ../deploy/k8s/overlays/staging
```
