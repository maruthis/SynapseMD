# UI and MCP Integration

SynapseMD uses an **MCP server** as the integration contract for chatbot UIs. AnythingLLM and Open WebUI are interchangeable clients.

## Architecture

```
AnythingLLM / Open WebUI  →  MCP client  →  SynapseMD MCP Server  →  Platform services
```

The MCP server calls the same service layer as the FastAPI API (`AIService`, `CommandOrchestrator`, `RAGEngine`, `DataAccessLayer`, `audit_producer`). No business logic is duplicated in the UI layer.

## Compatibility Spike Results

| UI | MCP Support | Recommended Integration | Notes |
|---|---|---|---|
| **AnythingLLM** | Native MCP agent support | Direct MCP (stdio or SSE) | Best fit for local/dev; configure workspace MCP server |
| **Open WebUI** | Function tools / OpenAPI | MCP via external client or OpenAPI bridge | Use `deploy/openapi-bridge/` if UI cannot attach MCP directly |

**Default for local/dev:** AnythingLLM with direct MCP attachment.

**Fallback:** Open WebUI + OpenAPI function bridge exposing the same tool schemas.

## MCP Tool Contract

| Tool | Scope | Description |
|---|---|---|
| `list_commands` | `read:own` | List available health commands |
| `execute_command` | `write:own` | Run anonymized command through orchestrator |
| `get_profile_summary` | `read:own` | Summarize FHIR Patient resource for user |
| `query_fhir_records` | `read:own` | Query tenant-scoped FHIR bundle |
| `search_clinical_knowledge` | `read:own` | Search clinical + org RAG knowledge |
| `get_audit_summary` | `audit` | Recent audit events for tenant |
| `ai_status` | `read:own` | Module 21 AI feature status |
| `ai_analyze` | `write:own` | Comprehensive AI health analysis |
| `ai_predict` | `write:own` | Evidence-based health risk prediction |
| `ai_chat` | `write:own` | Natural-language health Q&A (PHI-safe) |
| `ai_report` | `write:own` | AI health report summary |

## Authentication

- `SYNAPSEMD_ACCESS_TOKEN` — bearer token from `/api/v1/auth/login`
- `SYNAPSEMD_TENANT_ID` — optional explicit tenant override (must match token)

Dev mode: use `synapsemd-mcp --dev-token` with pre-provisioned tenant credentials.

## Running Locally

```bash
# API only
cd platform && docker compose up api postgres

# Full stack with MCP + AnythingLLM
cd platform && docker compose --profile full up

# MCP server standalone (stdio)
synapsemd-mcp
```

## Open WebUI Bridge

If Open WebUI cannot attach MCP directly, run the OpenAPI bridge:

```bash
cd deploy/openapi-bridge && uvicorn bridge:app --port 8100
```

Configure Open WebUI custom tool endpoint: `http://openapi-bridge:8100/tools/invoke`

Example:

```bash
curl -X POST http://localhost:8100/tools/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool":"ai_predict","arguments":{"risk_type":"hypertension"}}'
```

## PHI boundary (chat UIs)

Chatbot clients (AnythingLLM, Open WebUI) MUST NOT become the system of record for PHI:

| Data | Stored in UI | Stored in platform |
|------|--------------|-------------------|
| FHIR bundles / profile JSON | ❌ No | ✅ Yes (`FHIR_LOCAL_STORE` / HAPI) |
| Raw lab/imaging records | ❌ No | ✅ Yes |
| Conversation transcripts | ⚠️ UI may cache chat text | Audit stores hashes only |
| JWT / session token | ✅ UI session only | Validated per request |

**Rules**

1. All health data reads/writes go through MCP tools or REST API — never paste PHI into UI system prompts
2. MCP `execute_command` and `ai_*` tools receive JWT; platform enforces tenant isolation
3. Open WebUI bridge passes Bearer token per request; no platform credentials in UI config files
4. Validate locally: [mydocs/qa/anythingllm-validation.md](../mydocs/qa/anythingllm-validation.md), [mydocs/qa/openwebui-validation.md](../mydocs/qa/openwebui-validation.md)
