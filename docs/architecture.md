# SynapseMD Architecture

System design, layer responsibilities, and deployment models. For **how to extend** the codebase (commands, skills, specialists, data, platform), see the **[Developer Guide](developer-guide.md)**.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Structure](#2-project-structure)
3. [Role of Each Folder](#3-role-of-each-folder)
4. [Separation of Concerns](#4-separation-of-concerns)
5. [Integration with Claude Code & Custom LLMs](#5-integration-with-claude-code--custom-llms)
6. [Repository Layout](#6-repository-layout)
7. [Deployment Models](#7-deployment-models)

---

## 1. Project Overview

SynapseMD is a **file-based personal health data management system** with an optional **enterprise platform** (`platform/`). Locally, health data lives in JSON files and intelligence is provided by slash commands, skills, and specialists executed by Claude Code (or any compatible LLM agent).

**Dual runtime:**

| Mode | Stack |
|------|-------|
| **Local CLI** | `commands/` + `skills/` + `specialists/` + `data/` |
| **Enterprise platform** | FastAPI + JWT + FHIR + MCP + anonymization + audit |

Both share Module 21 AI logic in `platform/synapsemd_platform/ai/prediction.py`.

**Core architecture (local CLI):**

```
User Input (natural language or slash commands)
        │
        ▼
  Claude Code CLI  ──── reads ────▶  commands/*.md   (what to do)
        │                            skills/*/SKILL.md (how to analyze)
        │                            specialists/*.md (domain expertise)
        │
        ├── reads/writes ──▶  data/                  (health records, JSON)
        └── generates   ──▶  Report/                 (HTML/Markdown output)
```

---

## 2. Project Structure

```
SynapseMD/
│
├── .claude/                    # Claude Code workspace (symlinks — see §5)
│   ├── settings.local.json
│   ├── commands      -> ../commands
│   ├── skills        -> ../skills
│   └── specialists   -> ../specialists
│
├── commands/                   # Source of truth — 60+ slash commands
├── skills/                     # Source of truth — 19 analyzer skills
├── specialists/                # Source of truth — medical specialty profiles
│
├── data-example/               # Example JSON templates for all domains
├── data/                       # Live user data (gitignored)
├── data/reference/             # Committed read-only lookup databases
│
├── scripts/                    # setup-data.sh, validation, Python helpers
├── tests/                      # unit/, integration/, e2e/, release/, eval/
├── docs/                       # Shipped documentation
├── platform/                   # Enterprise FastAPI package (synapsemd_platform)
├── deploy/                     # OpenAPI bridge, K8s manifests
│
├── Report/                     # Generated report output
├── README.md
└── pyproject.toml              # Root pytest config (≥95% coverage gate)
```

---

## 3. Role of Each Folder

### `commands/`

Slash command definitions — one `.md` file per command. Each file contains YAML frontmatter, execution steps, data contracts, and output format. Commands handle CRUD and delegate analysis to skills.

See [developer-guide.md § Recipe: Add a command](developer-guide.md#6-recipe-add-a-command).

### `skills/`

Analyzer modules for complex, multi-step analysis. Each skill lives in its own subdirectory with `SKILL.md` plus optional supporting docs and templates.

See [developer-guide.md § Recipe: Add a skill](developer-guide.md#7-recipe-add-a-skill).

### `specialists/`

Medical specialty consultation profiles used by `/consult` and `/specialist`. Flat `.md` files with safety red lines and output formats.

See [developer-guide.md § Recipe: Add a specialist](developer-guide.md#8-recipe-add-a-specialist).

### `data-example/` and `data/`

- `data-example/` — committed templates; copied to `data/` via `./scripts/setup-data.sh`
- `data/` — live user health data (gitignored)
- `data/reference/` — food, vaccine, and interaction lookup databases

Schema reference: [data-structures.md](data-structures.md).

### `platform/`

Enterprise FastAPI application: multi-tenant auth, FHIR storage, PHI anonymization, command orchestrator, MCP server, Module 21 AI REST routes, audit events.

See [platform/README.md](../platform/README.md), [release-gates.md](release-gates.md), and [compliance-controls.md](compliance-controls.md).

### `tests/`

266+ tests, ~99% coverage on `synapsemd_platform`. CI enforces ≥95% via `.github/workflows/platform-ci.yml`.

### `.claude/`

Claude Code runtime workspace. `commands/`, `skills/`, and `specialists/` are **symlinks** to repo root — not copies. Configuration in `settings.local.json` (tool permissions, MCP servers).

Repair symlinks: `./scripts/link-claude-workspace.sh`

---

## 4. Separation of Concerns

```
┌─────────────────┬───────────────────────────────────────────────────────┐
│ Layer           │ Responsibility                                        │
├─────────────────┼───────────────────────────────────────────────────────┤
│ Commands        │ User intent parsing, data CRUD, routing to skills     │
│ Skills          │ Deep analysis, pattern detection, HTML report output  │
│ Specialists     │ Clinical domain expertise, MDT consultation logic     │
│ Data (JSON)     │ Persistence — pure data, no logic                     │
│ Scripts         │ Batch processing, testing, standalone report gen      │
│ Platform        │ Auth, tenancy, PHI safety, REST/MCP, audit            │
│ .claude/        │ Runtime config — tool permissions, MCP, symlinks      │
└─────────────────┴───────────────────────────────────────────────────────┘
```

**Key design principles:**

1. **Commands own the UX** — arguments, data paths, output format; delegate analysis to skills.
2. **Skills own the analysis** — read widely, produce reports; no CRUD or user interaction.
3. **Specialists own the clinical lens** — interpret summaries in MDT flow, not raw dumps.
4. **Data files are schema-only** — compute derived values at runtime in commands/skills.
5. **Scripts are escape hatches** — deterministic logic shared with platform where possible.
6. **Platform adds safety** — anonymization, audit, guardrails; does not duplicate markdown specs.

Full extension rules: [developer-guide.md](developer-guide.md).

---

## 5. Integration with Claude Code & Custom LLMs

### How Claude Code Loads the System

1. Reads `.claude/settings.local.json` for allowed tools and MCP configuration
2. Registers files in `.claude/commands/` as slash commands (filename = command name)
3. Exposes skills via the Skill tool
4. Loads specialists for consultation commands

**Source of truth:** edit `commands/`, `skills/`, `specialists/` at repo root. Verify symlinks:

```bash
ls -la .claude/commands .claude/skills .claude/specialists
./scripts/link-claude-workspace.sh   # repair if needed
```

### Command Execution Flow

`/allergy add penicillin severe`:

1. Claude Code matches `allergy` → `.claude/commands/allergy.md`
2. YAML frontmatter defines `action` and `info` arguments
3. Claude follows numbered execution steps
4. Reads/writes `data/allergies.json`
5. Renders the defined output format

Validate command structure: `./scripts/validate-command.sh allergy`

### Skill Invocation

- Directly by user or via `Skill("health-trend-analyzer")` from a command step
- `SKILL.md` defines trigger conditions and analysis steps

### Custom or Self-Hosted LLM

Any agent with filesystem tools (Read, Write, Bash, Glob) and multi-step markdown following can run the system. For production multi-tenant deployments, use the built-in platform MCP server (`synapsemd-mcp`) rather than ad-hoc wrappers.

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `ANTHROPIC_MODEL` | Override Claude model | `claude-sonnet-4-6` |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max tokens per tool write | `32000` |
| `DATA_DIR` | Override data storage path | `./data/` |

---

## 6. Repository Layout

Current layout (symlinks active, platform integrated):

```
SynapseMD/
├── .claude/
│   ├── settings.local.json
│   ├── commands      -> ../commands
│   ├── skills        -> ../skills
│   └── specialists   -> ../specialists
├── commands/                         # 60+ commands
├── skills/                           # 19 skills
├── specialists/                      # flat .md files
├── data/                             # gitignored (except data/reference/)
├── data-example/
├── docs/                             # includes developer-guide.md
├── scripts/                          # setup-data.sh, link-claude-workspace.sh, validate-command.sh
├── tests/                            # 266+ tests
└── platform/                         # synapsemd_platform FastAPI package
```

**First-time setup:**

```bash
./scripts/setup-data.sh
./scripts/link-claude-workspace.sh
```

---

## 7. Deployment Models

### Model 1: Local CLI (default)

Users clone the repo and interact via Claude Code or Cursor:

```bash
git clone https://github.com/maruthis/SynapseMD.git
cd SynapseMD
./scripts/setup-data.sh
./scripts/link-claude-workspace.sh
claude
# /profile set 175 70 1990-01-01
```

**Pros:** No infrastructure, fully private, zero cost beyond API usage.  
**Cons:** Requires Claude Code CLI; no built-in web UI.

### Model 2: Enterprise Platform (REST + MCP)

Run the FastAPI platform for multi-tenant API access and chatbot integration:

```bash
cd platform
pip install -e ".[dev]"
uvicorn synapsemd_platform.api.main:app --reload
synapsemd-mcp   # MCP server for AnythingLLM / Open WebUI
```

```
UI / Chatbot ──▶ MCP or REST ──▶ synapsemd_platform ──▶ FHIR + audit
                                      │
                                      ├── CommandOrchestrator (generic commands)
                                      ├── AIService (Module 21 /ai routes)
                                      └── PHI anonymization + guardrails
```

Docs: [platform/README.md](../platform/README.md), [ui-mcp-integration.md](ui-mcp-integration.md), [local-development.md](local-development.md).

Docker/K8s: `deploy/` directory.

### Model 3: Custom LLM Agent Framework

Commands and skills are plain markdown. LangChain, CrewAI, or internal agents can load command files as system prompts and attach filesystem tools. The markdown specs remain identical — only tool implementations change.

For cloud storage, replace local filesystem tools with tenant-scoped object storage while keeping command/skill definitions unchanged.

### Production Considerations

| Concern | Recommendation |
|---------|----------------|
| **Auth** | Platform JWT with tenant isolation |
| **Data isolation** | Per-tenant FHIR namespace |
| **Privacy** | Anonymize before LLM; audit logs store hashes only |
| **Model costs** | Route by command complexity (`HealthLLMRouter`) |
| **Clinical safety** | Guardrails + human review queue for critical commands |
| **Compliance** | See [release-gates.md](release-gates.md), [clinical-safety-policy.md](clinical-safety-policy.md) |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [getting-started.md](getting-started.md) | End-user setup and first-week workflow |
| [developer-guide.md](developer-guide.md) | Extension recipes and checklists |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | PR checklist and setup |
| [data-structures.md](data-structures.md) | JSON schema reference |
| [platform/README.md](../platform/README.md) | Enterprise platform API and deployment |
| [ui-mcp-integration.md](ui-mcp-integration.md) | MCP and chatbot wiring |
