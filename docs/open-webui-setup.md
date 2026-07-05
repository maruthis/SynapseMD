# Open WebUI Setup Guide

Connect [Open WebUI](https://github.com/open-webui/open-webui) to SynapseMD so you can chat with your health data in a web browser instead of using slash commands in Claude Code.

**Audience:** End users and admins setting up a local or self-hosted chat UI.

**Related:** [Getting Started](getting-started.md) · [UI & MCP Integration](ui-mcp-integration.md) · [AnythingLLM steps in Getting Started](getting-started.md#optional--chat-ui-anythingllm-or-open-webui)

---

## How it works

Open WebUI does **not** attach to SynapseMD’s MCP server directly. It uses the **OpenAPI bridge** — a small HTTP service that exposes the same 11 health tools as REST endpoints:

```text
You (browser)  →  Open WebUI (:3000)  →  OpenAPI bridge (:8100)  →  SynapseMD platform
```

Your health records stay on the **platform** (FHIR store). Open WebUI only shows chat messages — it must not become your health record system.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Docker Desktop** (or Docker Engine + Compose) | Recommended — easiest path |
| **SynapseMD repo cloned** | `git clone https://github.com/maruthis/SynapseMD.git` |
| **~4 GB free RAM** | For API + bridge + Open WebUI |
| **Web browser** | Chrome, Firefox, Safari, Edge |

You do **not** need Claude Code for this workflow. You still need a SynapseMD **platform account** (tenant + user) and a login token.

---

## Step 1 — Start the platform stack

From the repo root:

```bash
cd platform
docker compose --profile full up --build
```

Wait until these services are healthy:

| Service | URL | Purpose |
|---------|-----|---------|
| SynapseMD API | http://localhost:8000/docs | Auth, health data, AI engine |
| OpenAPI bridge | http://localhost:8100/health | Tool gateway for Open WebUI |
| Open WebUI | http://localhost:3000 | Chat interface |

Verify the bridge:

```bash
curl http://localhost:8100/health
# {"status":"healthy","service":"synapsemd-openapi-bridge"}

curl http://localhost:8100/tools
# {"tools":["list_commands","execute_command",...,"ai_chat","ai_report"]}
```

---

## Step 2 — Create your account and get a login token

Open WebUI tools call the bridge with a **Bearer token** from SynapseMD login. Create a tenant and user once:

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

Test the bridge with your token:

```bash
curl -s -X POST http://localhost:8100/tools/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool":"ai_status","arguments":{}}' | python3 -m json.tool
```

You should see AI status JSON (enabled features, data sources, disclaimer).

---

## Step 3 — Open Open WebUI

1. Go to **http://localhost:3000**
2. On first visit, create your **Open WebUI** local account (name + password)
   - This is separate from your SynapseMD platform login
   - Default Compose config uses `WEBUI_AUTH=false` for quick local dev; enable auth in production

3. Select a chat model (Open WebUI uses its own LLM provider settings for the conversational layer; SynapseMD tools supply your **health data**)

---

## Step 4 — Add SynapseMD tools in Open WebUI

Open WebUI connects to external capabilities via **Functions** (Python tool plugins). Add one function per SynapseMD tool you want, or start with the bundled examples below.

### 4a. Open the Functions editor

1. In Open WebUI, go to **Workspace** → **Functions** (or **Admin Panel** → **Functions**, depending on version)
2. Click **+ Create Function**
3. Paste a function from the examples below
4. Save and **enable** the function for your workspace

### 4b. Set your bridge URL and token

Inside each function, update these two values:

```python
self.bridge_url = "http://openapi-bridge:8100"   # Docker Compose (Open WebUI container)
# self.bridge_url = "http://host.docker.internal:8100"  # If Open WebUI runs on host, not in Docker
self.token = "PASTE_YOUR_SYNAPSEMD_JWT_HERE"
```

| Where Open WebUI runs | Bridge URL |
|----------------------|------------|
| Docker Compose (`--profile full`) | `http://openapi-bridge:8100` |
| Installed on your Mac/PC (bridge in Docker) | `http://localhost:8100` or `http://host.docker.internal:8100` |

### 4c. Example function — AI health chat

Paste this as a new Function in Open WebUI:

```python
"""
title: SynapseMD Health Chat
author: SynapseMD
version: 0.1.0
description: Ask questions about your stored health data (PHI-safe via SynapseMD platform).
required_open_webui_version: 0.3.0
"""

import json
import urllib.request
import urllib.error


class Tools:
    def __init__(self):
        self.bridge_url = "http://openapi-bridge:8100"
        self.token = "PASTE_YOUR_SYNAPSEMD_JWT_HERE"

    def _invoke(self, tool: str, arguments: dict) -> dict:
        payload = json.dumps({"tool": tool, "arguments": arguments}).encode()
        req = urllib.request.Request(
            f"{self.bridge_url}/tools/invoke",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())

    def ask_about_my_health(self, question: str) -> str:
        """
        Ask a natural-language question about your SynapseMD health records.
        :param question: Your health question, e.g. "What are my main trends this quarter?"
        """
        result = self._invoke("ai_chat", {"query": question})
        return json.dumps(result, indent=2)
```

### 4d. Example function — risk prediction

```python
"""
title: SynapseMD Risk Prediction
author: SynapseMD
version: 0.1.0
"""

import json
import urllib.request


class Tools:
    def __init__(self):
        self.bridge_url = "http://openapi-bridge:8100"
        self.token = "PASTE_YOUR_SYNAPSEMD_JWT_HERE"

    def predict_health_risk(
        self,
        risk_type: str = "hypertension",
    ) -> str:
        """
        Predict evidence-based health risk from your stored data.
        :param risk_type: One of hypertension, diabetes, cardiovascular,
                          nutritional_deficiency, sleep_disorders
        """
        payload = json.dumps({
            "tool": "ai_predict",
            "arguments": {"risk_type": risk_type},
        }).encode()
        req = urllib.request.Request(
            f"{self.bridge_url}/tools/invoke",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.dumps(json.loads(resp.read().decode()), indent=2)
```

### 4e. Enable tools in chat

1. Start a **new chat**
2. Open the **Tools** / **+** menu and enable your SynapseMD functions
3. Ask naturally, e.g.:
   - *“Use SynapseMD to check my hypertension risk”*
   - *“Ask about my health: how has my sleep been?”*

The Open WebUI model will call your function, which invokes SynapseMD on the platform.

---

## Step 5 — Add a health disclaimer system prompt (recommended)

In Open WebUI **Settings** → **Personalization** → **System Prompt**, add:

```text
You are a health assistant connected to SynapseMD. Always use SynapseMD tools for
health data — never invent lab values or diagnoses. All output is informational
only, not medical advice. Tell the user to consult a qualified healthcare
professional for medical decisions. In emergencies, direct them to emergency services.
```

---

## Available SynapseMD tools

All tools are invoked via `POST /tools/invoke` with `"tool": "<name>"`.

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

CLI equivalents: see [commands/ai.md](../commands/ai.md).

---

## PHI and privacy rules

| Rule | Why |
|------|-----|
| **Do not paste lab reports or SSNs into the system prompt** | Prompts may be stored by Open WebUI; use tools for data access |
| **Health data lives on the platform**, not in Open WebUI | Open WebUI is a chat shell only |
| **Rotate tokens** if shared or leaked | Re-login at `/api/v1/auth/login` |
| **Enable Open WebUI auth** in production | Default dev Compose disables it |
| **Back up platform data**, not chat logs | FHIR store under Docker volume `fhir_data` |

Full policy: [ui-mcp-integration.md](ui-mcp-integration.md#phi-boundary-chat-uis).

---

## Troubleshooting

### `Connection refused` to bridge

```bash
docker compose --profile full ps    # openapi-bridge should be Up
curl http://localhost:8100/health
```

If Open WebUI is in Docker, use `http://openapi-bridge:8100`, not `localhost`.

### `401 Bearer token required`

- Token missing or expired — run the login step again
- Token not pasted correctly in the Function (no extra spaces)

### `403` or scope errors

- User role may lack permission (e.g. `get_audit_summary` needs auditor scope)
- Use `patient` role tools: `ai_chat`, `ai_predict`, `get_profile_summary`

### Tools run but return empty data

- Platform may have no FHIR records yet for your user
- Seed data via API or migrate from local `data/` (see [platform/README.md](../platform/README.md))
- Check: `curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/ai/status`

### Open WebUI model ignores functions

- Confirm functions are **enabled** in the chat Tools menu
- Use explicit phrasing: *“Use the SynapseMD Health Chat tool to …”*
- Pick a model that supports tool/function calling in Open WebUI

### Token expires

Re-run the login curl from Step 2 and update the token in your Functions.

---

## Production checklist

- [ ] Enable Open WebUI authentication (`WEBUI_AUTH=true`)
- [ ] Use HTTPS for Open WebUI and the bridge (reverse proxy)
- [ ] Do not hard-code JWTs in Functions — use Open WebUI **Valves** or secrets injection
- [ ] Set strong SynapseMD passwords; use short-lived tokens where possible
- [ ] Run release validation: [release-gates.md](release-gates.md)

---

## What to read next

| Document | Purpose |
|----------|---------|
| [Getting Started — Chat UI section](getting-started.md#optional--chat-ui-anythingllm-or-open-webui) | AnythingLLM + overview |
| [ui-mcp-integration.md](ui-mcp-integration.md) | Architecture and MCP tool contract |
| [platform/README.md](../platform/README.md) | API reference and Docker profiles |
| [safety-guidelines.md](safety-guidelines.md) | Medical disclaimers |
