# AnythingLLM MCP Validation Checklist

Manual QA for local/dev release gate. Date: __________ Operator: __________

## Prerequisites

- [ ] Platform API running (`docker compose --profile core up`)
- [ ] MCP server available (`synapsemd-mcp` or compose profile `mcp`)
- [ ] AnythingLLM installed with MCP agent support
- [ ] Test tenant created; JWT obtained via `/api/v1/auth/login`

## Setup

- [ ] Configure workspace MCP server pointing to `synapsemd-mcp`
- [ ] Set `SYNAPSEMD_ACCESS_TOKEN` in MCP server env
- [ ] Restart AnythingLLM workspace

## Tool smoke tests

| Tool | Pass | Notes |
|------|------|-------|
| `list_commands` | [ ] | Includes `ai` |
| `get_profile_summary` | [ ] | |
| `ai_status` | [ ] | Returns disclaimer |
| `ai_predict` | [ ] | `risk_type=hypertension` |
| `execute_command` | [ ] | `command=goal` |

## Security checks

- [ ] Invalid/expired JWT rejected
- [ ] Chat history in AnythingLLM does not contain raw email/phone from test data
- [ ] Audit events recorded for tool calls (check `/admin/audit`)

## Result

- [ ] **PASS** — ready for staging UI integration
- [ ] **FAIL** — document blockers below

Blockers:
