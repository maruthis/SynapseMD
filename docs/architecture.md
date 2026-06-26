# SynapseMD: Architecture & Developer Guide

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Project Structure](#2-project-structure)
3. [Role of Each Folder](#3-role-of-each-folder)
4. [Separation of Concerns](#4-separation-of-concerns)
5. [Integration with Claude Code & Custom LLMs](#5-integration-with-claude-code--custom-llms)
6. [Optimizing the Project Structure](#6-optimizing-the-project-structure)
7. [Deployment & UI Integration](#7-deployment--ui-integration)

---

## 1. Project Overview

SynapseMD is a **file-based personal health data management system** built on top of the Claude Code CLI. It has no traditional backend or database — all health data lives in local JSON files, and all intelligence is provided by slash commands and skills executed by Claude Code (or any compatible LLM).

**What it is not:** a web app, a React/Next.js project, or a REST API server. The `package.json` at the root is a publishing manifest only — all script entries are no-ops.

**Core architecture layers:**

```
User Input (natural language or slash commands)
        │
        ▼
  Claude Code CLI  ──── reads ────▶  commands/*.md   (what to do)
        │                            skills/*.md      (how to analyze)
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
├── .claude/                    # Active Claude Code workspace (see §3)
│   ├── settings.local.json     # Permissions, MCP servers, allowed tools
│   ├── commands/               # Mirror of root commands/ (59 files)
│   ├── skills/                 # Mirror of root skills/ (20 dirs)
│   └── specialists/            # Mirror of root specialists/
│
├── commands/                   # Source-of-truth for slash command definitions
├── skills/                     # Source-of-truth for skill (analyzer) definitions
├── specialists/                # Medical specialist consultation templates
│
├── data-example/               # Example/template JSON data for all modules
│   ├── *.json                  # Health tracker files (~60 files)
│   ├── *-logs/                 # Historical log subdirectories
│   └── interactions/           # Drug interaction database
│
├── docs/                       # Project documentation
│   ├── marketing/              # Marketing content
│   └── plans/                  # Feature design plans
│
├── scripts/                    # Automation scripts
│   ├── *.py                    # Python: AI prediction, report generation
│   └── test*.sh                # Shell: integration tests
│
├── specialists/                # 18 medical specialty consultation templates
├── mydocs/                     # Internal docs and development roadmap
│   └── todo/                   # Not shipped to users
├── Report/                     # Output folder for generated health reports
│
├── README.md
├── package.json                # Publishing manifest only (no runtime deps)
└── LICENSE
```

---

## 3. Role of Each Folder

### `commands/`
Slash command definitions — one `.md` file per command. Each file contains:
- **YAML frontmatter**: `description`, `arguments` (name, description, required)
- **Execution steps**: numbered instructions Claude follows when the command is invoked
- **Data contracts**: exact file paths read/written (`data/allergies.json`, etc.)
- **Output format**: what Claude should render to the user

Commands are user-facing entry points. They handle CRUD on health data and delegate deep analysis to skills.

**Example:** `/allergy add penicillin severe` → Claude reads `commands/allergy.md`, extracts intent, writes to `data/allergies.json`.

### `skills/`
Analyzer modules for complex, multi-step analysis. Each skill lives in its own subdirectory:

```
skills/health-trend-analyzer/
├── SKILL.md          # Main skill definition (trigger conditions, steps, output)
├── algorithms.md     # Statistical methods used
├── data-sources.md   # Which data files are read and why
├── examples.md       # Sample inputs/outputs
└── templates/
    └── charts-config.js  # ECharts configuration for HTML visualizations
```

Skills are invoked either directly (`/health-trend-analyzer`) or called internally by commands when analysis depth is needed. They use `glob()` patterns to aggregate data across multiple JSON files and produce rich HTML/Markdown reports.

### `specialists/`
Medical specialty consultation profiles. Each `.md` file defines:
- The specialist's role and clinical focus
- Key health indicators to assess
- Analysis principles and safety boundaries
- Output format (specialist report sections)

Used by the `/consult` command (MDT — multi-disciplinary team) and `/specialist` command (single-specialty). The `consultation-coordinator.md` orchestrates parallel specialist opinions into a unified report.

### `data-example/`
Fully populated example JSON files showing the exact schema for every health domain. Serves three purposes:
1. **Template**: copy `data-example/` to `data/` to bootstrap a new user's records
2. **Testing**: used by shell scripts in `scripts/` for integration tests
3. **Reference**: shows developers the exact field names and data types expected

Each tracker file (e.g., `fitness-tracker.json`) contains both current state and historical arrays. Log subdirectories (`fitness-logs/YYYY-MM/`) store daily snapshot files.

### `docs/`
Static documentation. Notable files:
- `data-structures.md` — comprehensive JSON schema reference for all tracker files
- `drug-interaction-database.md` — A/B/C/D/X severity classification system
- `safety-guidelines.md` — medical boundaries and disclaimer requirements
- `womens-health-*.md` — implementation notes for the women's health module

### `scripts/`
- **Python scripts** (`ai_prediction.py`, `generate_health_report.py`): standalone data processing; can be called from commands via `Bash(python3:*)` permissions
- **Shell test scripts** (`test*.sh`): end-to-end integration tests that invoke commands and assert on file state

### `.claude/`
Claude Code's working directory. Contents are **mirrors** of the root `commands/`, `skills/`, and `specialists/` folders, kept in sync by `cp` commands. The key configuration is `settings.local.json`:

```json
{
  "permissions": {
    "allow": ["Bash(python3:*)", "Bash(node:*)", "Bash(cp:*)"]
  },
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["claude-flow", "ruv-swarm"]
}
```

MCP servers (`claude-flow`, `ruv-swarm`) enable advanced multi-agent coordination — used by `/consult` to run specialist consultations in parallel.

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
│ .claude/        │ Runtime config — tool permissions, MCP, mirrors       │
└─────────────────┴───────────────────────────────────────────────────────┘
```

**Key design principles:**

1. **Commands own the UX.** A command file is the contract between the user and the system. It defines what arguments are accepted, what data is touched, and what the user sees. Commands should not embed analysis logic — they delegate to skills.

2. **Skills own the analysis.** A skill reads widely across data files, applies algorithms (defined in `algorithms.md`), and outputs structured reports. Skills have no concept of user interaction — they are called with data and return analysis.

3. **Specialists own the clinical lens.** Specialists don't read raw data directly — they receive summaries from commands or skills and apply domain-specific interpretation. This mirrors how a real MDT works: each specialist reviews a case summary, not raw lab printouts.

4. **Data files are schema-only.** JSON tracker files contain no logic, no computed fields. All derivation (BMI from height/weight, TDEE from BMR × activity) happens in commands or skills at runtime.

5. **Scripts are escape hatches.** Python and shell scripts handle things Claude can't do inline — heavy numerical computation, batch report generation, CI testing. They are called from commands via whitelisted `Bash()` tool permissions.

---

## 5. Integration with Claude Code & Custom LLMs

### How Claude Code Loads the System

When a user opens the project in Claude Code, the CLI:
1. Reads `.claude/settings.local.json` for allowed tools and MCP server configuration
2. Registers all files in `.claude/commands/` as slash commands (filename without `.md` = command name)
3. Makes skills available as invocable sub-agents via the Skill tool
4. Loads specialists as additional context for consultation commands

**The `.claude/` directory is the active workspace.** Root `commands/`, `skills/`, and `specialists/` are the source of truth and are symlinked into `.claude/` — no manual sync is needed after edits.

```bash
# Verify symlinks (should show ../commands, ../skills, ../specialists)
ls -la .claude/commands .claude/skills .claude/specialists
```

Edit files in the root directories (e.g. `commands/medication.md`); changes are immediately visible at `.claude/commands/medication.md`.

### How Commands Are Executed

When a user types `/allergy add penicillin severe`:
1. Claude Code matches `allergy` to `.claude/commands/allergy.md`
2. The YAML frontmatter defines the expected `action` and `info` arguments
3. Claude reads the execution steps and follows them as instructions
4. It reads/writes `data/allergies.json` using the Read and Write tools
5. It renders the output format defined at the bottom of the command file

### How Skills Are Invoked

Skills are triggered either:
- **Directly** by the user: `/health-trend-analyzer` or via a command that calls `Skill("health-trend-analyzer")`
- **Automatically** by commands when they detect that analysis depth is needed

The `SKILL.md` file contains both the trigger conditions (natural language patterns that should activate the skill) and the step-by-step analysis logic.

### Using a Custom or Self-Hosted LLM

The system is LLM-agnostic — any model that supports tool use (Read, Write, Bash, Glob) can run it. To switch models:

**Option A — Claude API with a different model:**
```bash
# In your Claude Code config or environment
export ANTHROPIC_MODEL=claude-opus-4-8
```

**Option B — OpenAI-compatible API (e.g., local Ollama, Azure OpenAI):**

The commands and skills are plain markdown instructions. Any LLM agent framework that can:
- Read files from a local filesystem
- Write files to a local filesystem
- Execute bash commands (for Python scripts)
- Follow multi-step markdown instructions

...can execute this system. Example with LangChain or CrewAI:

```python
from langchain.tools import ReadFileTool, WriteFileTool
from langchain.agents import AgentExecutor

# Load a command file as the agent's system prompt
with open("commands/allergy.md") as f:
    system_prompt = f.read()

agent = AgentExecutor(
    tools=[ReadFileTool(), WriteFileTool(), BashTool()],
    llm=your_llm,          # any LangChain-compatible LLM
    system_message=system_prompt
)
agent.run("add penicillin severe allergy")
```

**Option C — MCP server (recommended for production):**

The project already has MCP integration configured (`claude-flow`, `ruv-swarm`). Expose the `commands/` and `data/` directories via an MCP file server, then connect any MCP-compatible LLM client.

### Environment Variable Reference

| Variable | Purpose | Default |
|---|---|---|
| `ANTHROPIC_MODEL` | Override Claude model | `claude-sonnet-4-6` |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max tokens per tool write | `32000` |
| `DATA_DIR` | Override data storage path | `./data/` |

---

## 6. Optimizing the Project Structure

> **Status: Implemented.** The optimizations below are active in this repository.

### Duplication Problem (Resolved)

The root `commands/`, `skills/`, and `specialists/` directories were manually copied to `.claude/`. This is now replaced with symlinks — a single source of truth with no sync step.

```bash
.claude/commands    -> ../commands
.claude/skills      -> ../skills
.claude/specialists -> ../specialists
```

### Current Folder Layout

```
SynapseMD/
│
├── .claude/
│   ├── settings.local.json
│   ├── commands      -> ../commands    (symlink)
│   ├── skills        -> ../skills      (symlink)
│   └── specialists   -> ../specialists (symlink)
│
├── commands/                         # Source of truth
├── skills/                           # Source of truth
├── specialists/                      # Source of truth (flat .md files)
│
├── data/                             # Live user data (gitignored except reference/)
│   ├── reference/                    # Committed read-only databases
│   │   ├── food-database.json
│   │   └── vaccine-database.json
│   └── (copied from data-example/ via scripts/setup-data.sh)
│
├── data-example/                     # Example tracker templates only
├── mydocs/                           # Internal docs, roadmap, Chinese README
│   └── todo/                         # Development roadmap (not shipped)
│
├── docs/                             # Shipped documentation
├── scripts/                          # Automation (incl. setup-data.sh)
└── platform/                         # Enterprise API (optional)
```

### Applied Optimizations

1. **Symlinks** — `.claude/` points to root `commands/`, `skills/`, `specialists/`.
2. **Gitignore `data/`** — user health data excluded; `data/reference/` is committed.
3. **Consolidated docs** — `user-guide.md` and `data-structures.md` are the canonical English docs (`.en` duplicates removed).
4. **Moved `todo/`** — relocated to `mydocs/todo/` (internal roadmap, not part of shipped product).
5. **Split reference databases** — `food-database.json`, `vaccine-database.json`, etc. live in `data/reference/`.
6. **Normalized specialists** — both root and `.claude/specialists/` use flat `.md` files via symlink.

**First-time data setup:**

```bash
./scripts/setup-data.sh
```

---

## 7. Deployment & UI Integration

### Deployment Model 1: Local CLI (Current)

The simplest deployment — users clone the repo and interact via Claude Code terminal:

```bash
git clone https://github.com/huifer/SynapseMD
cd SynapseMD
cp -r data-example/ data/     # Bootstrap data directory
claude                         # Open Claude Code
# Then use: /profile set 175 70 1990-01-01
```

**Pros:** No infrastructure, fully private, zero cost beyond API usage.
**Cons:** Requires Claude Code CLI installed, no web UI.

### Deployment Model 2: MCP Server + Any UI

Expose the health system as an MCP server so any MCP-compatible frontend can call it:

```
UI (web app / mobile) ──HTTP──▶ MCP Server ──▶ Commands/Skills ──▶ data/
```

**Step 1 — Start an MCP file server:**
```bash
# Using the built-in claude-flow MCP (already in settings.local.json)
npx @anthropic-ai/claude-flow serve \
  --root /path/to/SynapseMD \
  --port 3001
```

**Step 2 — Connect your UI:**
```javascript
// Example: call /allergy list from a React app
const response = await fetch('http://localhost:3001/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    command: 'allergy',
    args: { action: 'list' }
  })
});
const result = await response.json();
```

### Deployment Model 3: REST API Wrapper

Wrap the command execution in a lightweight Express/FastAPI server:

```python
# api.py
from fastapi import FastAPI
from pathlib import Path
import subprocess, json

app = FastAPI()

@app.post("/command/{name}")
async def run_command(name: str, args: dict):
    # Load command definition
    cmd_file = Path(f"commands/{name}.md")
    if not cmd_file.exists():
        return {"error": "command not found"}
    
    # Call Claude API with command as system prompt + user args
    import anthropic
    client = anthropic.Anthropic()
    
    prompt = cmd_file.read_text()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=prompt,
        messages=[{"role": "user", "content": json.dumps(args)}],
        tools=[read_tool, write_tool, glob_tool]  # filesystem tools
    )
    return {"result": message.content}
```

```bash
uvicorn api:app --reload --port 8000
```

**Then call from any frontend:**
```javascript
// React / Next.js / mobile
const res = await fetch('/api/command/allergy', {
  method: 'POST',
  body: JSON.stringify({ action: 'list' })
});
```

### Deployment Model 4: Serverless (Vercel / AWS Lambda)

For a hosted multi-user deployment:

```
User Browser ──▶ Vercel Edge Function ──▶ Anthropic API
                        │                       │
                        ▼                       ▼
                  User's data on          Command/Skill
                  S3 / R2 / DB            definitions
```

Replace the local filesystem tools with cloud storage equivalents:

| Local tool | Cloud equivalent |
|---|---|
| `Read(data/allergies.json)` | `S3.getObject(userId, "allergies.json")` |
| `Write(data/allergies.json)` | `S3.putObject(userId, "allergies.json")` |
| `Glob(data/**/*.json)` | `S3.listObjects(userId, prefix="")` |

The command and skill `.md` files remain identical — only the tool implementations change.

### Key Considerations for Production

| Concern | Recommendation |
|---|---|
| **Auth** | JWT per user; prefix all data paths with `data/{userId}/` |
| **Data isolation** | Each user gets their own `data/` namespace in storage |
| **Rate limiting** | Cache command definitions; don't re-read `.md` files per request |
| **Privacy** | Never log request bodies (contain medical data); encrypt at rest |
| **Model costs** | Commands with large data reads (consultation, trend analysis) can consume 10k+ tokens; add a usage cap |
| **Streaming** | Use the Anthropic streaming API for long-running commands (`/consult`, `/report`) so the UI shows progress |
