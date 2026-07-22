# AnythingLLM Setup Guide

Connect [AnythingLLM](https://anythingllm.com) to SynapseMD so you can chat with your health data through MCP agent tools.

**Audience:** End users and admins setting up a local AnythingLLM (Docker or Desktop) against SynapseMD on Docker Desktop.

**Related:** [Getting Started](getting-started.md) · [UI & MCP Integration](ui-mcp-integration.md) · [Open WebUI setup](open-webui-setup.md)

**AnythingLLM MCP docs:** [Overview](https://docs.anythingllm.com/mcp-compatibility/overview) · [Docker](https://docs.anythingllm.com/mcp-compatibility/docker) · [Desktop](https://docs.anythingllm.com/mcp-compatibility/desktop)

---

## How it works

```text
You (browser / Desktop)
    →  AnythingLLM (:3001 or Desktop app)
         →  SynapseMD MCP (SSE :8081/sse  or  stdio synapsemd-mcp)
              →  Platform API / FHIR / AI tools
```

| Piece | URL / note |
|-------|------------|
| SynapseMD API | http://localhost:8000 — auth + health (`/health`) |
| MCP health | http://localhost:8081/health |
| MCP SSE | http://localhost:8081/sse |
| AnythingLLM (Compose) | http://localhost:3001 |

Your health records stay on the **platform**. AnythingLLM is a chat shell — do not paste lab PDFs or SSNs into system prompts.

---

## Auth: what `SYNAPSEMD_ACCESS_TOKEN` is

SynapseMD MCP tools authenticate with a **SynapseMD login JWT**, not an AnythingLLM API key.

| | |
|--|--|
| **Is** | `access_token` from `POST http://localhost:8000/api/v1/auth/login` (usually starts with `eyJ…`) |
| **Is not** | AnythingLLM API key / Desktop password |
| **Is not** | `JWT_SECRET` (signing key used by the API/MCP containers) |
| **Is not** | Tenant ID or user password |

### Where to set it (by path)

| Setup | Where `SYNAPSEMD_ACCESS_TOKEN` goes | AnythingLLM config |
|-------|--------------------------------------|--------------------|
| **Path A** — Compose AnythingLLM + Docker MCP (SSE) | **`platform/.env`** → injected into `mcp` container | SSE URL only: `http://mcp:8081/sse` |
| **Path B** — Desktop + Docker MCP (SSE) | **`platform/.env`** → injected into `mcp` container | SSE URL only: `http://localhost:8081/sse` |
| **Path C** — Desktop + host stdio | **`env` block** in `anythingllm_mcp_servers.json` | command + `env` including the JWT |

For **Paths A and B**, do **not** put the JWT in AnythingLLM. Desktop/Compose only need the SSE URL; the MCP container already holds the token.

**File location:** `platform/.env` (next to `platform/docker-compose.yml`).  
Do **not** use a `.env` at the **repo root** — Compose reads `platform/.env`.

After changing the token:

```bash
cd platform
docker compose --profile mcp up -d mcp
# or: docker compose --profile full up -d mcp
```

Verify the container has it **without printing the secret**:

```bash
docker exec platform-mcp-1 printenv SYNAPSEMD_ACCESS_TOKEN | wc -c
# should be > 0 (typically ~350+)
```

Avoid `printenv SYNAPSEMD_ACCESS_TOKEN` alone in shared terminals — it prints the full JWT.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Docker Desktop** running | For SynapseMD MCP (+ optional Compose AnythingLLM) |
| **SynapseMD repo cloned** | `git clone https://github.com/maruthis/SynapseMD.git` |
| **AnythingLLM** | Compose service **or** Desktop app |
| **~2–4 GB free RAM** | `mcp` profile ≈ 2 GB; `full` stack more |
| **Tool-capable LLM** in AnythingLLM | Agents need a model that can call tools |

---

## Step 1 — Start SynapseMD (API + MCP)

From the repo:

```bash
cd platform
docker compose --profile mcp up --build -d
```

For AnythingLLM **inside** Compose as well:

```bash
docker compose --profile full up --build -d
```

Verify:

```bash
curl -sS http://localhost:8000/health
# {"status":"healthy","service":"synapsemd-platform"}

curl -sS http://localhost:8081/health
# {"status":"ok","transport":"sse","server":"synapsemd-mcp"}
```

> **Note:** Use `http://localhost:8000/health` — `/api/v1/health` is **not** a valid route (404).

| Compose profile | Services |
|-----------------|----------|
| `mcp` | `postgres`, `api`, `mcp` |
| `full` | Above + AnythingLLM, Open WebUI, bridge, etc. |

---

## Step 2 — Create a SynapseMD account and JWT

### Shell tips (common gotchas)

1. **`VAR=$(curl …)` prints nothing** — the body is stored in the variable. Use `echo "$VAR"` to inspect.
2. **`tenant_id` must be a real UUID** from step 2 below. Do **not** paste the literal text `YOUR_TENANT_ID` — that causes API validation errors and then `KeyError: 'access_token'` in Python.
3. Login **requires** `tenant_id` in the JSON body.

Run this block (prints each step):

```bash
cd /Users/maruti/Documents/MaruGit/SynapseMD/platform   # or: cd platform

# 1. Create tenant (prints JSON — copy the "id" field)
curl -sS -X POST http://localhost:8000/api/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"AnythingLLM Health","plan":"starter"}'
echo

# 2. Capture tenant + show ID (use THIS value as TENANT_ID)
TENANT=$(curl -sS -X POST http://localhost:8000/api/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"AnythingLLM Health 2","plan":"starter"}')
echo "TENANT=$TENANT"
TENANT_ID=$(echo "$TENANT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "TENANT_ID=$TENANT_ID"
# Example shape: 913f761d-371d-431d-85be-e9d66f036557

# 3. Register user
curl -sS -X POST "http://localhost:8000/api/v1/auth/tenants/$TENANT_ID/users" \
  -H "Content-Type: application/json" \
  -d '{"email":"me@example.com","password":"securepass1","role":"patient"}'
echo

# 4. Login — use $TENANT_ID from step 2 (must be a UUID)
TOKEN=$(curl -sS -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"me@example.com\",\"password\":\"securepass1\",\"tenant_id\":\"$TENANT_ID\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo "TOKEN length=${#TOKEN}"
# Optional: echo "$TOKEN"  # keep private
```

If step 3 says the email already exists, reuse that user and only re-run **login** with the **same** `TENANT_ID` the user was registered under.

If login fails with `KeyError: 'access_token'`, print the raw response (do not assume success):

```bash
curl -sS -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"me@example.com\",\"password\":\"securepass1\",\"tenant_id\":\"$TENANT_ID\"}"
echo
```

### Put the JWT on the MCP container (Paths A & B — SSE)

```bash
cd platform
printf 'SYNAPSEMD_ACCESS_TOKEN=%s\n' "$TOKEN" > .env

docker compose --profile mcp up -d mcp
# or: docker compose --profile full up -d mcp

docker exec platform-mcp-1 printenv SYNAPSEMD_ACCESS_TOKEN | wc -c
```

Compose also sets `JWT_SECRET=dev-secret-change-in-production` on `api` and `mcp` so tokens from `/auth/login` validate correctly. That secret is **not** the same as `SYNAPSEMD_ACCESS_TOKEN`.

---

## Step 3 — Configure AnythingLLM MCP

Pick **one** path below.

| Your AnythingLLM | Recommended MCP mode | Config URL / command |
|------------------|----------------------|----------------------|
| **Compose** (`localhost:3001`) | SSE | `http://mcp:8081/sse` |
| **Desktop** app | SSE | `http://localhost:8081/sse` |
| **Desktop** app | stdio (optional) | Host `synapsemd-mcp` binary |

AnythingLLM reads:

```text
plugins/anythingllm_mcp_servers.json
```

inside its storage directory. Opening **Agent Skills → MCP Servers** creates the file if missing. Then edit it and click **Refresh** in the UI.

---

### Path A — AnythingLLM in Docker Compose + SynapseMD SSE (recommended)

**Token:** already in `platform/.env` (Step 2). Not in the JSON below.

1. Open **http://localhost:3001** and finish the AnythingLLM setup wizard.
2. Create a **Workspace** (e.g. `SynapseMD Health`).
3. Choose a **tool-capable** LLM (agents need function/tool calling).
4. Open **Agent Skills → MCP Servers** once (creates empty config).
5. Write the config **inside** the AnythingLLM container:

```bash
docker exec -it platform-anythingllm-1 bash

mkdir -p /app/server/storage/plugins
cat > /app/server/storage/plugins/anythingllm_mcp_servers.json << 'EOF'
{
  "mcpServers": {
    "SynapseMD": {
      "type": "sse",
      "url": "http://mcp:8081/sse"
    }
  }
}
EOF
exit
```

**Why `http://mcp:8081`?** AnythingLLM and MCP share the Compose network. `localhost` *inside* the AnythingLLM container is **not** your Mac.

6. In the UI: **Agent Skills → MCP Servers → Refresh**.
7. Confirm **SynapseMD** is running and lists tools (see [Available tools](#available-synapsemd-mcp-tools)).
8. In chat, use **Agent** mode / `@agent`, for example:
   - `@agent Use SynapseMD ai_status`
   - `@agent Predict my hypertension risk with SynapseMD`
   - `@agent Ask SynapseMD: summarize my health profile`

---

### Path B — AnythingLLM Desktop + Docker MCP (SSE)

**Token:** set only in **`platform/.env`**, then recreate `mcp` (Step 2).  
**Do not** add `SYNAPSEMD_ACCESS_TOKEN` to AnythingLLM Desktop settings or to the JSON `env` block for this path.

1. Confirm MCP is up and has the token:

   ```bash
   curl -sS http://localhost:8081/health
   docker exec platform-mcp-1 printenv SYNAPSEMD_ACCESS_TOKEN | wc -c
   ```

2. Install/open [AnythingLLM Desktop](https://anythingllm.com).
3. Open **Agent Skills → MCP Servers** so `anythingllm_mcp_servers.json` is created.
4. Edit the Desktop storage file (path varies by OS), typically on macOS:

```text
~/Library/Application Support/anythingllm-desktop/storage/plugins/anythingllm_mcp_servers.json
```

Contents (URL only — **no** JWT here):

```json
{
  "mcpServers": {
    "SynapseMD": {
      "type": "sse",
      "url": "http://localhost:8081/sse"
    }
  }
}
```

Here **`localhost` is correct** — Desktop runs on the host and reaches Docker’s published port `8081`.

5. **Refresh** MCP servers in Agent Skills → use `@agent` as in Path A.

---

### Path C — Desktop + stdio `synapsemd-mcp` on the host (optional)

Use when AnythingLLM should spawn the MCP process itself. For this path the JWT goes in the JSON **`env`** block (AnythingLLM passes it to the child process).

```bash
cd platform
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[mcp]"
which synapsemd-mcp
```

`anythingllm_mcp_servers.json`:

```json
{
  "mcpServers": {
    "SynapseMD": {
      "command": "/ABSOLUTE/PATH/TO/platform/.venv/bin/synapsemd-mcp",
      "args": [],
      "env": {
        "SYNAPSEMD_ACCESS_TOKEN": "PASTE_LOGIN_ACCESS_TOKEN_HERE",
        "JWT_SECRET": "dev-secret-change-in-production",
        "DATABASE_URL": "postgresql+asyncpg://synapsemd:synapsemd@localhost:5432/synapsemd",
        "AUDIT_USE_MEMORY": "true",
        "LLM_DEFAULT_PROVIDER": "mock"
      }
    }
  }
}
```

- Use the **full path** to `synapsemd-mcp`.
- `SYNAPSEMD_ACCESS_TOKEN` = same login JWT as Step 2.
- `JWT_SECRET` must match the API Compose value (`dev-secret-change-in-production`).
- Postgres must be reachable at `localhost:5432`.

Then **Refresh** in Agent Skills.

---

## Available SynapseMD MCP tools

| Tool | Scope | Description |
|------|-------|-------------|
| `list_commands` | `read:own` | List available health commands |
| `execute_command` | `write:own` | Run a command through the orchestrator |
| `get_profile_summary` | `read:own` | FHIR patient profile summary |
| `query_fhir_records` | `read:own` | Tenant-scoped FHIR query |
| `search_clinical_knowledge` | `read:own` | Clinical / org RAG search |
| `get_audit_summary` | `audit` | Recent audit events |
| `ai_status` | `read:own` | Module 21 AI feature status |
| `ai_analyze` | `write:own` | Multi-dimensional health analysis |
| `ai_predict` | `write:own` | Risk prediction (e.g. hypertension) |
| `ai_chat` | `write:own` | Natural-language health Q&A |
| `ai_report` | `write:own` | AI health report summary |

Full contract: [ui-mcp-integration.md](ui-mcp-integration.md).

---

## Day-to-day commands

```bash
cd platform

# Start MCP stack
docker compose --profile mcp up -d

# Logs
docker compose --profile mcp logs -f mcp

# Recreate MCP after updating platform/.env token
docker compose --profile mcp up -d mcp

# Stop (keep volumes)
docker compose --profile mcp stop
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|--------|-----|
| Curl “no response” | Output captured in `VAR=$(curl …)` | `echo "$VAR"` or run curl without `$()` |
| `KeyError: 'access_token'` | Login failed (bad/missing UUID, wrong password) | Print raw login JSON; set `TENANT_ID` to a real UUID from tenant create |
| Literal `YOUR_TENANT_ID` in curl | Placeholder not replaced | Use `$TENANT_ID` from `echo "TENANT_ID=…"` (UUID form) |
| `/api/v1/health` → 404 | Wrong path | Use `/health` |
| MCP Stopped (Compose AnythingLLM) | Wrong URL | Use `http://mcp:8081/sse`, not `localhost` |
| Desktop can’t connect | MCP not published / wrong URL | `curl localhost:8081/health`; use `http://localhost:8081/sse` |
| URL starts with `https://` | Modal default | Change to **`http://`** |
| `SYNAPSEMD_ACCESS_TOKEN is required` | Token not on MCP process | Set **`platform/.env`**, recreate `mcp`; confirm with `printenv … \| wc -c` |
| Token in repo-root `.env` but MCP empty | Wrong file | Use **`platform/.env`** |
| `Invalid token` | JWT secret mismatch or expired | Re-login; ensure MCP `JWT_SECRET` matches API; recreate `mcp` |
| Tools listed but model never calls them | Not in Agent mode / weak model | Use `@agent`; pick a stronger tool-capable LLM |
| Empty health data | No FHIR/records for user | Seed/migrate via API ([platform/README.md](../platform/README.md)) |
| Config not applied | File edited but UI not refreshed | Agent Skills → **Refresh** |

Debug:

```bash
docker compose --profile full ps   # or --profile mcp
docker compose --profile mcp logs mcp --tail 80
curl -sS http://localhost:8081/health
docker exec platform-mcp-1 printenv SYNAPSEMD_ACCESS_TOKEN | wc -c
curl -sS -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/ai/status
```

---

## PHI and privacy

| Rule | Why |
|------|-----|
| Do not paste lab reports / SSNs into AnythingLLM prompts | Chat may be stored by the UI |
| Health data lives on SynapseMD | AnythingLLM is presentation only |
| Keep JWTs in `platform/.env` / Path C `env`, not in chat | Rotate on leak via re-login |
| Prefer `wc -c` over printing tokens | Avoid leaking JWTs in terminal logs |
| Prefer short-lived tokens in shared environments | Limit blast radius |

Validation checklist: [mydocs/qa/anythingllm-validation.md](../mydocs/qa/anythingllm-validation.md).

---

## Quick reference

| AnythingLLM runs as | SynapseMD MCP | Token location | `anythingllm_mcp_servers.json` |
|---------------------|---------------|----------------|--------------------------------|
| Compose (`:3001`) | Compose SSE | `platform/.env` | `"type":"sse","url":"http://mcp:8081/sse"` |
| Desktop | Compose SSE | `platform/.env` | `"type":"sse","url":"http://localhost:8081/sse"` |
| Desktop | Host stdio | JSON `env` block | `"command":"/…/synapsemd-mcp","env":{…}` |

---

## What to read next

| Document | Purpose |
|----------|---------|
| [getting-started.md](getting-started.md) | End-user overview |
| [ui-mcp-integration.md](ui-mcp-integration.md) | MCP tool contract |
| [open-webui-setup.md](open-webui-setup.md) | Alternate chat UI |
| [platform/docker-compose.profiles.md](../platform/docker-compose.profiles.md) | Compose profiles |
| [safety-guidelines.md](safety-guidelines.md) | Medical disclaimers |
