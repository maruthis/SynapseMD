# Docker Compose Profiles

| Profile | Services | Use Case |
|---------|----------|----------|
| `core` | api, postgres | Minimal API development |
| `mcp` | api, postgres, mcp (SSE on :8081) | MCP server development |
| `infra` | postgres, hapi-fhir, redpanda, vault | Infrastructure only |
| `full` | All services | Full local stack with UI |

## Commands

```bash
# Core API
docker compose --profile core up

# MCP development
docker compose --profile mcp up

# Full stack with AnythingLLM + Open WebUI
docker compose --profile full up
```

Set `SYNAPSEMD_ACCESS_TOKEN` in `.env` after logging in via the API.
