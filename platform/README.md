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

## LLM Choice

LLM selection has two layers: **which provider** to call, and **which model ID** that provider uses.

### Provider (environment)

Set in `platform/.env` (template: `.env.example`):

```env
LLM_DEFAULT_PROVIDER=mock    # mock | anthropic | openai | google
ANTHROPIC_API_KEY=
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_BAA_SIGNED=false
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_BAA_SIGNED=false
GOOGLE_API_KEY=
GOOGLE_BASE_URL=https://generativelanguage.googleapis.com
GOOGLE_BAA_SIGNED=false
APP_ENV=development
```

| Setting | Role |
|---------|------|
| `LLM_DEFAULT_PROVIDER` | Default backend used by `create_provider()` in `llm/providers.py` |
| `*_API_KEY` / `*_BASE_URL` | Credentials and endpoints for that provider |
| `*_BAA_SIGNED` | Required `true` when `APP_ENV` is `staging` or `production` (see [docs/baa-tracking.md](../docs/baa-tracking.md)) |

Also configured in:

| Location | Typical value |
|----------|----------------|
| `docker-compose.yml` (`api` / `mcp`) | `LLM_DEFAULT_PROVIDER=mock` |
| `deploy/k8s/overlays/staging/` | `mock` |
| `deploy/k8s/overlays/production/` | `anthropic` (+ BAA flags `true`) |

`mock` returns deterministic stub text — fine for local Docker and unit tests.

### Model ID (routing table)

Concrete model names are chosen by **`HealthLLMRouter`** in `synapsemd_platform/llm/router.py` based on command complexity and data sensitivity (e.g. `claude-haiku-4-5`, `claude-sonnet-4-6`, `claude-opus-4-8`, with fallbacks such as `gpt-4o`).

The command orchestrator calls `LLMOrchestrator.execute(prompt, decision)` with that `RoutingDecision`. To change which Claude/GPT/etc. model is used for a given complexity tier, edit `ROUTING_TABLE` in `llm/router.py`.

### What this does *not* control

| Path | LLM selection |
|------|----------------|
| Module 21 `/api/v1/ai/*` predict/analyze | Mostly local scoring in `ai/prediction.py` (`synapsemd-ai`), not the external provider |
| Local CLI slash commands | Model configured in Cursor / Claude Code |
| AnythingLLM / Open WebUI chat | Their own model settings; SynapseMD MCP tools that hit the orchestrator still use `LLM_DEFAULT_PROVIDER` + the router |

## Tests

```bash
# From repo root (recommended — enforces ≥95% coverage gate)
cd .. && pytest -v

# Release gate + eval regression suites
pytest tests/release/ tests/eval/ -v

# Platform package only
pytest -v
```

Current baseline: **266 tests**, **≥98% coverage** on `synapsemd_platform`.

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
