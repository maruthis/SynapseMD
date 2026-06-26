# UI and MCP Integration

SynapseMD uses an **MCP server** as the integration contract for chatbot UIs. AnythingLLM and Open WebUI are interchangeable clients.

## Architecture

```
AnythingLLM / Open WebUI  →  MCP client  →  SynapseMD MCP Server  →  Platform services
```

The MCP server calls the same service layer as the FastAPI API (`CommandOrchestrator`, `RAGEngine`, `DataAccessLayer`, `audit_producer`). No business logic is duplicated in the UI layer.

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

## Authentication

MCP clients pass a SynapseMD JWT via environment variable or request header:

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

Configure Open WebUI custom tool endpoint: `http://openapi-bridge:8100/tools/execute_command`
