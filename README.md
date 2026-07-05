# SynapseMD — Personal Health Information System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform CI](https://img.shields.io/badge/tests-266%20passed-brightgreen.svg)](platform/README.md)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A598%25-brightgreen.svg)](pyproject.toml)

SynapseMD is a file-based personal health data management system with an optional **enterprise platform** for multi-tenant, PHI-safe deployments. Use Claude Code slash commands locally, or run the FastAPI platform with REST API and MCP tools for chatbot UIs.

**GitHub**: https://github.com/maruthis/SynapseMD

> **Disclaimer**: This project is not affiliated with, endorsed by, or associated with [Anthropic](https://www.anthropic.com/) or [Claude.ai](https://claude.ai/). It is an independent open-source project developed by [SynapseMD](https://www.synapsemd.com/).
>
> **Note**: Local image recognition may use GLM's `mcp__4_5v_mcp__analyze_image` where configured.

---

## Two Ways to Use SynapseMD

| Mode | Best for | Entry point |
|------|----------|-------------|
| **CLI (local)** | Personal health repo, Cursor/Claude workflows | `/commands` + `data/` JSON files |
| **Platform** | Multi-tenant API, audit, chatbot integration | `platform/` FastAPI + MCP server |

Both modes share the same Module 21 AI prediction engine (`platform/synapsemd_platform/ai/prediction.py`).

---

## How SynapseMD is different

SynapseMD isn’t a typical app where “the code” lives in one layer. The product is the extension surface:

| Artifact | What it defines |
| --- | --- |
| commands/ | User-facing behavior, CRUD, routing |
| skills/ | Deep analysis and reports |
| specialists/ | Clinical lens for MDT |
| data-example/ + data/ | Schemas and persistence |
| scripts/ | Deterministic logic escape hatches |
| platform/ | REST/MCP/tenant execution (optional but growing) |

## System Features

### Local CLI

- File-based JSON storage — no database required for personal use
- Medical report image recognition and structured extraction
- MDT consultation across 13 medical specialties
- Drug interaction detection (A/B/C/D/X severity levels)
- Radiation dose tracking, surgery history, discharge summaries
- **Module 21 AI**: analyze, predict, chat, report, status via `/ai` commands

### Enterprise Platform

- Multi-tenant JWT auth with RBAC and tenant isolation
- FHIR-backed health data with anonymization before LLM calls
- REST API at `/api/v1/*` including `/api/v1/ai/*`
- MCP server with 11 tools (including `ai_status`, `ai_predict`, `ai_analyze`, `ai_chat`, `ai_report`)
- Audit events (hash-only PHI storage), medical guardrails, human review queue
- Docker Compose profiles and Kubernetes overlays for staging/production

---

## Repository Structure

```
SynapseMD/
├── commands/              # Slash command definitions (/ai, /profile, /consult, …)
├── skills/                # Analyzer skills (ai-analyzer, nutrition, sleep, …)
├── specialists/           # Medical specialty skill definitions
├── data/                  # Local health data (gitignored — use setup script)
├── data-example/          # Templates seeded by ./scripts/setup-data.sh
├── scripts/               # CLI helpers (ai_prediction.py, setup-data.sh, …)
├── platform/              # Enterprise FastAPI package (synapsemd_platform)
│   └── synapsemd_platform/
│       ├── ai/            # AIPredictionEngine, tenant adapter, AIService
│       ├── api/           # REST routes (/ai, /auth, /commands, admin)
│       ├── mcp/           # MCP tools + shared dispatch
│       └── services/      # Command orchestrator, tenant service
├── tests/                 # unit/, integration/, e2e/, release/, eval/
├── deploy/                # OpenAPI bridge, K8s manifests
├── docs/                  # User guide, release gates, runbooks, compliance
└── pyproject.toml         # Root pytest config (≥95% coverage gate)
```

---

## Quick Start (Local CLI)

**New user?** Follow the step-by-step guide: **[docs/getting-started.md](docs/getting-started.md)**

Summary:

1. Install [Claude Code](https://claude.ai/code) or [Cursor](https://cursor.com/)
2. Clone this repo and run `./scripts/setup-data.sh` and `./scripts/link-claude-workspace.sh`
3. Open the project in Claude Code or Cursor
4. Set profile: `/profile set 175 70 1990-01-01`
5. Save a report: `/save-report /path/to/image.jpg`
6. Run AI analysis: `/ai analyze last_quarter`
7. Query records: `/query all`

Full command reference: [docs/user-guide.md](docs/user-guide.md)

---

## Quick Start (Platform)

```bash
cd platform
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn synapsemd_platform.api.main:app --reload
```

API docs: http://localhost:8000/docs

```bash
# From repo root — full test suite (266 tests, ≥95% coverage)
pytest -v

# MCP server (after login token)
export SYNAPSEMD_ACCESS_TOKEN=<jwt-from-/api/v1/auth/login>
synapsemd-mcp
```

See [platform/README.md](platform/README.md) for AI API, MCP tools, and Docker/K8s usage.

---

## Module 21 — AI Health Assistant

| CLI | REST API | MCP tool |
|-----|----------|----------|
| `/ai status` | `GET /api/v1/ai/status` | `ai_status` |
| `/ai analyze` | `POST /api/v1/ai/analyze` | `ai_analyze` |
| `/ai predict` | `POST /api/v1/ai/predict` | `ai_predict` |
| `/ai chat` | `POST /api/v1/ai/chat` | `ai_chat` |
| `/ai report` | `POST /api/v1/ai/report` | `ai_report` |

Risk predictions: hypertension, diabetes, cardiovascular, nutritional deficiency, sleep disorders (evidence-based scoring models).

Docs: [commands/ai.md](commands/ai.md) · [docs/ui-mcp-integration.md](docs/ui-mcp-integration.md) · [docs/release-gates.md](docs/release-gates.md)

---

## Core Commands

| Command | Description |
|---------|-------------|
| `/profile` | User height, weight, birth date |
| `/save-report` | Save biochemical or imaging reports |
| `/medication` | Medication plans and records |
| `/interaction` | Drug interaction detection |
| `/query` | Multi-condition health data queries |
| `/consult` | Multi-disciplinary consultation (13 specialties) |
| `/specialist` | Single specialty consultation |
| `/ai` | AI analyze, predict, chat, report, status |

Full list: 60+ commands in [commands/](commands/).

---

## Documentation

| Topic | Link |
|-------|------|
| **Getting started (end users)** | [docs/getting-started.md](docs/getting-started.md) |
| **Open WebUI setup** | [docs/open-webui-setup.md](docs/open-webui-setup.md) |
| **Developer guide** | [docs/developer-guide.md](docs/developer-guide.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| User guide | [docs/user-guide.md](docs/user-guide.md) |
| Data structures | [docs/data-structures.md](docs/data-structures.md) |
| Architecture | [docs/architecture.md](docs/architecture.md) |
| Platform & AI API | [platform/README.md](platform/README.md) |
| MCP / UI integration | [docs/ui-mcp-integration.md](docs/ui-mcp-integration.md) |
| Release gates | [docs/release-gates.md](docs/release-gates.md) |
| Drug interactions | [docs/drug-interaction-database.md](docs/drug-interaction-database.md) |
| Safety guidelines | [docs/safety-guidelines.md](docs/safety-guidelines.md) |
| Technical details | [docs/technical-details.md](docs/technical-details.md) |


---

## Testing & Quality

```bash
pytest -v                              # Full suite (266 tests)
pytest tests/release/ tests/eval/ -v   # Release gates + model eval
```

- **Coverage**: ≥95% enforced on `synapsemd_platform` (current: ~99%)
- **CI**: `.github/workflows/platform-ci.yml` — lint, tests, release/eval jobs
- **E2E**: tenant → AI analyze → audit trail verification in `tests/e2e/`

---

## Data Privacy

**Local CLI**: All data stays on your filesystem. No cloud uploads. No external database.

**Platform**: Tenant-scoped storage, JWT auth, PHI anonymization before LLM calls, audit logs store hashes only. See [docs/runbooks/phi-handling.md](docs/runbooks/phi-handling.md).

---

## Safety Statement

This system follows medical safety principles:

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis

All AI and analysis output is for reference only. Consult a qualified healthcare professional for medical decisions. In an emergency, seek immediate medical attention.

---

## License

Open source under the [MIT License](LICENSE).

**Important**: For personal health management and informational use only — not a basis for medical diagnosis.
