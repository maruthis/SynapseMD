# Open WebUI Setup Guide (v0.10.2)

Connect [Open WebUI](https://github.com/open-webui/open-webui) **v0.10.2** to SynapseMD so you can chat with your health data in a browser instead of using slash commands in Claude Code.

**Audience:** End users and admins setting up a local or self-hosted chat UI.

**Tested against:** Open WebUI [`v0.10.2`](https://github.com/open-webui/open-webui/releases/tag/v0.10.2) (Compose image: `ghcr.io/open-webui/open-webui:v0.10.2`).

**Related:** [Getting Started](getting-started.md) · [UI & MCP Integration](ui-mcp-integration.md) · [AnythingLLM steps](getting-started.md#optional--chat-ui-anythingllm-or-open-webui)

---

## How it works (v0.10.2)

In Open WebUI **v0.10.x**, external capabilities come from several layers. SynapseMD fits best as a **Workspace Tool** (or optionally via **MCP / OpenAPI** connections):

| Integration | Where in UI (v0.10.2) | SynapseMD path | When to use |
|-------------|----------------------|----------------|-------------|
| **Workspace Tools** (recommended) | **Workspace → Tools** | Python `Tools` class → OpenAPI bridge `:8100` | Full control, Valves for JWT, works offline from the chat model |
| **Native MCP (HTTP/SSE)** | **Settings → Connections** (or **Admin Settings → Tools**) | `synapsemd-mcp` SSE `:8081/sse` | Prefer MCP-native clients; same 11 tools as the platform |
| **OpenAPI tool server** | **Settings → ➕ Tools** / **Admin Settings → Tools** | Bridge OpenAPI at `:8100` | Quick discovery of REST endpoints; auth/CORS need care |

```text
You (browser)
    →  Open WebUI v0.10.2 (:3000)
         ├─ Workspace Tools  →  OpenAPI bridge (:8100)  →  SynapseMD API
         └─ MCP connection   →  synapsemd-mcp SSE (:8081) →  SynapseMD services
```

Your health records stay on the **platform** (FHIR store). Open WebUI only shows chat messages — it must not become your health record system.

> **Terminology note (v0.10):** **Tools** (`class Tools`) give the model callable abilities. **Functions** are a different plugin family (Pipes, Filters, Actions, and the new **Event** functions in 0.10.2). For SynapseMD health tools, use **Workspace → Tools**, not Functions.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Docker Desktop** (or Docker Engine + Compose) | Recommended |
| **SynapseMD repo cloned** | `git clone https://github.com/maruthis/SynapseMD.git` |
| **~4 GB free RAM** | API + bridge + MCP + Open WebUI |
| **A chat model that supports tool calling** | e.g. GPT-4o / strong OpenAI-compatible models; many small local models struggle with native tools |
| **Web browser** | Chrome, Firefox, Safari, Edge |

You do **not** need Claude Code for this workflow. You still need a SynapseMD **platform account** (tenant + user) and a login token.

---

## Step 1 — Start the platform stack

From the repo root:

```bash
cd platform
docker compose --profile full up --build -d
```

Compose pins Open WebUI to **v0.10.2**. Wait until these are up:

| Service | URL | Purpose |
|---------|-----|---------|
| SynapseMD API | http://localhost:8000/docs | Auth, health data, AI engine |
| OpenAPI bridge | http://localhost:8100/health | REST tool gateway |
| MCP (SSE) | http://localhost:8081/health | Native MCP for Connections |
| Open WebUI | http://localhost:3000 | Chat UI (v0.10.2) |

Verify:

```bash
curl -s http://localhost:8100/health
# {"status":"healthy","service":"synapsemd-openapi-bridge"}

curl -s http://localhost:8100/tools
# {"tools":["list_commands","execute_command",...,"ai_chat","ai_report"]}

curl -s http://localhost:8081/health
# {"status":"ok","transport":"sse","server":"synapsemd-mcp"}
```

Confirm the UI version (footer / **Settings → About**, or image tag):

```bash
docker compose --profile full images open-webui
# expect ghcr.io/open-webui/open-webui:v0.10.2
```

---

## Step 2 — Create your account and get a login token

Open WebUI tools call SynapseMD with a **Bearer token** from platform login. Create a tenant and user once:

```bash
# 1. Create tenant
TENANT=$(curl -s -X POST http://localhost:8000/api/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"My Health","plan":"starter"}')
TENANT_ID=$(echo "$TENANT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Tenant ID: $TENANT_ID"

# 2. Register user
curl -s -X POST "http://localhost:8000/api/v1/auth/tenants/$TENANT_ID/users" \
  -H "Content-Type: application/json" \
  -d '{"email":"me@example.com","password":"securepass1","role":"patient"}'

# 3. Login and save token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"me@example.com\",\"password\":\"securepass1\",\"tenant_id\":\"$TENANT_ID\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Save this token securely:"
echo "$TOKEN"
```

**Keep this token private.** Anyone with it can access your tenant’s health tools until it expires.

Test the bridge:

```bash
curl -s -X POST http://localhost:8100/tools/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool":"ai_status","arguments":{}}' | python3 -m json.tool
```

You should see AI status JSON (enabled features, data sources, disclaimer).

| Symptom | Cause | Fix |
|---------|--------|-----|
| `401 Invalid or expired token` | Token missing/wrong, or bridge JWT secret ≠ API | Re-login; Compose must set the same `JWT_SECRET` on `api` and `openapi-bridge` |
| Empty / `Internal Server Error` | Older bridge bug | `docker compose --profile full up -d --build openapi-bridge` |
| Connection refused | Bridge not running | `docker compose --profile full up -d openapi-bridge` |
| `Expecting value` from `json.tool` | Non-JSON error body | Drop `\| python3 -m json.tool` once and read the raw response |

---

## Step 3 — Open Open WebUI v0.10.2

1. Go to **http://localhost:3000**
2. First visit:
   - With default Compose (`WEBUI_AUTH=false`), you land in the chat UI without a login wall (dev only)
   - In production, set `WEBUI_AUTH=true` and create the first **admin** account when prompted
3. Configure a **model provider** (if none is set):
   - **Admin Settings → Connections** (or **Settings → Connections**) for Ollama / OpenAI-compatible APIs
   - v0.10.2 also supports `OPENAI_API_CONFIGS` / `OLLAMA_API_CONFIGS` env vars for per-connection config
4. Pick a model that supports **native tool / function calling**

Open WebUI’s own account is **separate** from your SynapseMD platform login. SynapseMD auth is the JWT from Step 2.

---

## Step 4 — Add SynapseMD as a Workspace Tool (recommended)

This is the most reliable path on **v0.10.2**.

### 4a. Create the tool

1. Open **Workspace → Tools** (left sidebar / workspace switcher — **not** Functions)
2. Click **＋** / **Create**
3. Paste the toolkit below
4. **Save**, then open the tool’s **Valves** and set:
   - `BRIDGE_URL` — see table below
   - `ACCESS_TOKEN` — paste your SynapseMD JWT from Step 2
5. Ensure the tool is **Enabled**

| Where Open WebUI runs | `BRIDGE_URL` |
|----------------------|--------------|
| Docker Compose (`--profile full`) — tool runs **inside** Open WebUI container | `http://openapi-bridge:8100` |
| Open WebUI on host; bridge in Docker | `http://localhost:8100` or `http://host.docker.internal:8100` |

### 4b. Example toolkit (Valves — v0.10.2)

```python
"""
title: SynapseMD Health Tools
author: SynapseMD
version: 0.2.0
description: Call SynapseMD health tools via the OpenAPI bridge (PHI stays on the platform).
required_open_webui_version: 0.10.2
"""

import json
import urllib.error
import urllib.request

from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        BRIDGE_URL: str = Field(
            default="http://openapi-bridge:8100",
            description="SynapseMD OpenAPI bridge base URL",
        )
        ACCESS_TOKEN: str = Field(
            default="",
            description="SynapseMD JWT from /api/v1/auth/login",
        )
        TIMEOUT_SECONDS: int = Field(
            default=120,
            description="HTTP timeout for bridge calls",
        )

    def __init__(self) -> None:
        self.valves = self.Valves()

    def _invoke(self, tool: str, arguments: dict) -> str:
        if not self.valves.ACCESS_TOKEN.strip():
            return json.dumps(
                {"error": "Set ACCESS_TOKEN in this tool's Valves (SynapseMD JWT)."}
            )
        payload = json.dumps({"tool": tool, "arguments": arguments}).encode()
        req = urllib.request.Request(
            f"{self.valves.BRIDGE_URL.rstrip('/')}/tools/invoke",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.valves.ACCESS_TOKEN.strip()}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.valves.TIMEOUT_SECONDS) as resp:
                return json.dumps(json.loads(resp.read().decode()), indent=2)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            return json.dumps({"error": f"HTTP {exc.code}", "detail": body}, indent=2)
        except Exception as exc:  # noqa: BLE001
            return json.dumps({"error": str(exc)})

    def ai_status(self) -> str:
        """Get SynapseMD Module 21 AI feature status for the authenticated user."""
        return self._invoke("ai_status", {})

    def ask_about_my_health(self, question: str) -> str:
        """
        Ask a natural-language question about your SynapseMD health records.
        :param question: Your health question, e.g. "What are my main trends this quarter?"
        """
        return self._invoke("ai_chat", {"query": question})

    def predict_health_risk(self, risk_type: str = "hypertension") -> str:
        """
        Predict evidence-based health risk from your stored data.
        :param risk_type: One of hypertension, diabetes, cardiovascular,
                          nutritional_deficiency, sleep_disorder
        """
        return self._invoke("ai_predict", {"risk_type": risk_type})

    def analyze_my_health(self, time_range: str = "last_quarter") -> str:
        """
        Run multi-dimensional AI health analysis.
        :param time_range: e.g. last_month, last_quarter, last_year
        """
        return self._invoke("ai_analyze", {"time_range": time_range})

    def get_profile_summary(self) -> str:
        """Summarize the FHIR patient profile for the authenticated user."""
        return self._invoke("get_profile_summary", {})
```

### 4c. Enable tools in a chat (v0.10.2 UI)

1. Start a **new chat** and select your tool-capable model
2. Click the **＋** control on the **message input** (bottom-left of the composer)
3. Toggle on **SynapseMD Health Tools** (and any other tools you need)
4. For best results with OpenAI-class models, open **Chat Controls → Advanced Params** and set **Function Calling** to **Native** (v0.10 defaults increasingly favor native/agentic tool use)
5. Ask naturally, e.g.:
   - *“Use SynapseMD to check my hypertension risk”*
   - *“Ask about my health: how has my sleep been?”*
   - *“Show my SynapseMD AI status”*

You should see a tool-server / tools indicator near the input when tools are active.

---

## Step 5 — Optional: Native MCP (SSE) connection

Open WebUI **v0.10** can attach MCP servers over HTTP/SSE without Python glue.

1. Ensure Compose MCP is healthy: `curl -s http://localhost:8081/health`
2. Set `SYNAPSEMD_ACCESS_TOKEN` on the `mcp` service (same JWT as Step 2), then recreate:

   ```bash
   # in platform/.env (do not commit)
   SYNAPSEMD_ACCESS_TOKEN=eyJ...
   docker compose --profile full up -d mcp
   ```

3. In Open WebUI:
   - **User-scoped:** **Settings → Connections** (or **Settings → ➕ Tools**, depending on build) → add MCP / tool server  
   - **Shared:** **Admin Settings → Tools** → add as a **global** tool server
4. URL guidance:

| Server type | URL to enter | Why |
|-------------|--------------|-----|
| **Global** (backend calls it) | `http://mcp:8081/sse` | Docker network name from Open WebUI container |
| **User** (browser calls it) | `http://localhost:8081/sse` | Browser reaches published port on your machine |

5. Use **`http://`**, not `https://` — the add-server modal often pre-fills HTTPS and fails on local stacks
6. Enable the MCP tools via the chat **＋** menu (global tools are **hidden until toggled**)

Official reference: [Open WebUI Tools](https://docs.openwebui.com/features/extensibility/plugin/tools/).

---

## Step 6 — Optional: Register the OpenAPI bridge as a tool server

FastAPI exposes `http://openapi-bridge:8100/openapi.json`. You can register the bridge under **Settings → ➕ Tools** or **Admin Settings → Tools**.

Caveats on **v0.10.2**:

- Discovery exposes endpoints like `/tools/invoke`, not eleven named SynapseMD tools — the model must pass `{"tool":"ai_chat",...}` correctly
- **User** tool servers are called from the **browser** → use `http://localhost:8100` and ensure the bridge allows CORS from `http://localhost:3000`
- **Global** tool servers are called from the **Open WebUI backend** → use `http://openapi-bridge:8100`
- Bearer auth must be configured on the connection if your UI build supports auth headers; otherwise prefer **Workspace Tools + Valves** (Step 4)

For most SynapseMD setups, Step 4 remains simpler and more reliable.

---

## Step 7 — Health disclaimer system prompt (recommended)

In Open WebUI **v0.10.2**:

1. Open **Settings → Personalization** (or the chat’s system-prompt field / model preset)
2. Add:

```text
You are a health assistant connected to SynapseMD. Always use SynapseMD tools for
health data — never invent lab values or diagnoses. All output is informational
only, not medical advice. Tell the user to consult a qualified healthcare
professional for medical decisions. In emergencies, direct them to emergency services.
```

---

## Available SynapseMD tools

All bridge tools are invoked via `POST /tools/invoke` with `"tool": "<name>"`.

| Tool | Example arguments | What it does |
|------|-------------------|--------------|
| `ai_status` | `{}` | AI feature status and data sources |
| `ai_chat` | `{"query": "How is my sleep?"}` | Natural-language Q&A on your data |
| `ai_analyze` | `{"time_range": "last_quarter"}` | Multi-dimensional health analysis |
| `ai_predict` | `{"risk_type": "hypertension"}` | Risk score for one condition |
| `ai_report` | `{"report_type": "comprehensive", "time_range": "last_quarter"}` | Structured health report |
| `get_profile_summary` | `{}` | Patient profile summary |
| `query_fhir_records` | `{"resource_type": "Observation", "limit": 20}` | Query FHIR records |
| `list_commands` | `{}` | List available health commands |
| `execute_command` | `{"command": "goal", "context_text": "..."}` | Run a health command |
| `search_clinical_knowledge` | `{"query": "hypertension guidelines"}` | Search clinical knowledge base |
| `get_audit_summary` | `{"limit": 20}` | Recent audit events (auditor role) |

CLI equivalents: [commands/ai.md](../commands/ai.md) · MCP contract: [ui-mcp-integration.md](ui-mcp-integration.md).

---

## PHI and privacy rules

| Rule | Why |
|------|-----|
| **Do not paste lab reports or SSNs into the system prompt** | Prompts may be stored by Open WebUI; use tools for data access |
| **Health data lives on the platform**, not in Open WebUI | Open WebUI is a chat shell only |
| **Store JWTs in Valves**, not in chat messages | Valves can be managed/rotated without editing chat history |
| **Rotate tokens** if shared or leaked | Re-login at `/api/v1/auth/login` |
| **Enable Open WebUI auth** in production | Default dev Compose disables it (`WEBUI_AUTH=false`) |
| **Back up platform data**, not chat logs | FHIR store under Docker volume `fhir_data` |

Full policy: [ui-mcp-integration.md](ui-mcp-integration.md#phi-boundary-chat-uis).

---

## Troubleshooting (v0.10.2)

### Wrong UI area — “I only see Functions”

You need **Workspace → Tools**. **Functions** (Pipes / Filters / Actions / **Event** in 0.10.2) are a different plugin system and will not host the `class Tools` examples above.

### `Connection refused` to bridge / MCP

```bash
docker compose --profile full ps
curl -s http://localhost:8100/health
curl -s http://localhost:8081/health
```

- Inside Workspace Tools running in the Open WebUI container: use `http://openapi-bridge:8100`
- From the browser (user tool server): use `http://localhost:8100`

### Tool server won’t connect (https / localhost)

- Change `https://` → `http://` in the add-server modal
- **Global** servers: `localhost` means the **Open WebUI container**, not your Mac — use `openapi-bridge` / `mcp` hostnames
- **User** servers: `localhost` means your **browser’s machine**

### `401` / invalid token

- Token missing, expired, or not set in **Valves → ACCESS_TOKEN**
- Bridge and API must share `JWT_SECRET` (Compose already aligns these for `full`)

### `403` or scope errors

- `get_audit_summary` needs auditor scope
- Patient tools: `ai_chat`, `ai_predict`, `ai_status`, `get_profile_summary`

### Model ignores tools

- Confirm tools are toggled on via the chat **＋** menu
- Set **Chat Controls → Advanced Params → Function Calling → Native**
- Use a model with reliable native tool calling
- Ask explicitly: *“Use the SynapseMD ask_about_my_health tool to …”*

### Tools run but return empty health data

- No FHIR records for this user yet — migrate/seed via the API ([platform/README.md](../platform/README.md))
- Check: `curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/ai/status`

### Image drifted from v0.10.2

```bash
cd platform
docker compose --profile full pull open-webui
docker compose --profile full up -d open-webui
```

Ensure `docker-compose.yml` uses `ghcr.io/open-webui/open-webui:v0.10.2`, not `:main`.

---

## Production checklist

- [ ] Pin Open WebUI to a release tag (e.g. `v0.10.2`), not `:main`
- [ ] Enable Open WebUI authentication (`WEBUI_AUTH=true`)
- [ ] Use HTTPS for Open WebUI, bridge, and MCP (reverse proxy)
- [ ] Put JWTs in **Valves** / secrets — never hard-code in chat or git
- [ ] Prefer **global** tool servers only for endpoints safe to share across users
- [ ] Set strong SynapseMD passwords; rotate tokens on a schedule
- [ ] Run release validation: [release-gates.md](release-gates.md) · [openwebui-validation.md](../mydocs/qa/openwebui-validation.md)

---

## What to read next

| Document | Purpose |
|----------|---------|
| [Getting Started — Chat UI](getting-started.md#optional--chat-ui-anythingllm-or-open-webui) | AnythingLLM + overview |
| [ui-mcp-integration.md](ui-mcp-integration.md) | Architecture and MCP tool contract |
| [Open WebUI Tools docs](https://docs.openwebui.com/features/extensibility/plugin/tools/) | Official v0.10 tools / MCP / OpenAPI |
| [platform/README.md](../platform/README.md) | API reference and Docker profiles |
| [safety-guidelines.md](safety-guidelines.md) | Medical disclaimers |
