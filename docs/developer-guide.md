# SynapseMD Developer Guide

This guide is the **starting point for extending SynapseMD**. It explains where to edit, how layers interact, and the checklists to follow when adding commands, skills, specialists, data domains, scripts, or platform integrations.

For system diagrams and deployment models, see [architecture.md](architecture.md). For JSON field reference, see [data-structures.md](data-structures.md). For end-user command usage, see [user-guide.md](user-guide.md).

---

## Table of Contents

1. [Who this guide is for](#1-who-this-guide-is-for)
2. [Developer setup](#2-developer-setup)
3. [Architecture at a glance](#3-architecture-at-a-glance)
4. [Where to edit (source of truth)](#4-where-to-edit-source-of-truth)
5. [Extension decision tree](#5-extension-decision-tree)
6. [Recipe: Add a command](#6-recipe-add-a-command)
7. [Recipe: Add a skill](#7-recipe-add-a-skill)
8. [Recipe: Add a specialist](#8-recipe-add-a-specialist)
9. [Recipe: Add a data domain](#9-recipe-add-a-data-domain)
10. [Recipe: Add a script](#10-recipe-add-a-script)
11. [Recipe: Wire to the platform](#11-recipe-wire-to-the-platform)
12. [Safety and clinical modules](#12-safety-and-clinical-modules)
13. [Testing your extension](#13-testing-your-extension)
14. [Documentation map](#14-documentation-map)
15. [Common mistakes](#15-common-mistakes)

---

## 1. Who this guide is for

SynapseMD is designed to be **extended continuously**. Contributors add or enhance:

- **Commands** — user-facing slash commands (`/nutrition`, `/ai`, …)
- **Skills** — deep analyzers (`nutrition-analyzer`, `health-trend-analyzer`, …)
- **Specialists** — clinical lenses for MDT consultation (`cardiology`, `endocrinology`, …)
- **Data** — JSON schemas and example trackers in `data-example/`
- **Scripts** — deterministic Python/shell helpers
- **Platform** — REST/MCP exposure for multi-tenant deployments (optional)

You do **not** need to touch every layer for every feature. CLI-first extensions are valid; platform wiring is only required when the command must be reachable via API or MCP.

---

## 2. Developer setup

### Clone and bootstrap data

```bash
git clone https://github.com/maruthis/SynapseMD.git
cd SynapseMD
./scripts/setup-data.sh          # seeds data/ from data-example/
```

### Verify Claude Code workspace symlinks

Root directories are the **source of truth**. Claude Code reads from `.claude/`, which must symlink to them:

```bash
ls -la .claude/commands .claude/skills .claude/specialists
# Expected:
#   .claude/commands    -> ../commands
#   .claude/skills      -> ../skills
#   .claude/specialists -> ../specialists
```

If symlinks are missing (e.g. after a fresh clone on Windows, or if copies were made instead of links):

```bash
./scripts/link-claude-workspace.sh
```

**Rule:** Always edit `commands/`, `skills/`, and `specialists/` at the repo root. Never edit duplicate copies inside `.claude/` unless you are fixing the symlink setup itself.

### Open in Claude Code or Cursor

```bash
claude    # or open the repo in Cursor with Claude integration
```

Test a command: `/profile set 175 70 1990-01-01`

### Platform development (optional)

```bash
cd platform
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn synapsemd_platform.api.main:app --reload
pytest -v    # from repo root
```

See [local-development.md](local-development.md) and [platform/README.md](../platform/README.md).

---

## 3. Architecture at a glance

```
User input (slash command or natural language)
        │
        ▼
  Claude Code / Platform API
        │
        ├── reads ──▶  commands/*.md      (what to do — UX, CRUD, routing)
        │              skills/*/SKILL.md  (how to analyze — reports, patterns)
        │              specialists/*.md   (clinical lens — MDT opinions)
        │
        ├── reads/writes ──▶  data/*.json  (persistence — schema only, no logic)
        └── invokes ──▶  scripts/*.py      (deterministic computation)
```

| Layer | Owns | Must not |
|-------|------|----------|
| **Commands** | User intent, CRUD, output format, routing to skills | Embed deep analysis algorithms |
| **Skills** | Multi-file analysis, pattern detection, HTML/Markdown reports | Handle interactive UX or CRUD |
| **Specialists** | Domain clinical interpretation, safety boundaries | Read raw data directly in MDT flow |
| **Data (JSON)** | Stored values and history arrays | Logic, computed fields, business rules |
| **Scripts** | Batch math, report generation, test harnesses | Replace command UX |
| **Platform** | Auth, tenant isolation, PHI anonymization, audit, REST/MCP | Duplicate command markdown logic |

Full architecture and deployment models: [architecture.md](architecture.md).

---

## 4. Where to edit (source of truth)

| Path | Purpose | Committed? |
|------|---------|------------|
| `commands/` | Slash command definitions (one `.md` per command) | Yes |
| `skills/` | Analyzer skills (one subdirectory per skill) | Yes |
| `specialists/` | Medical specialty profiles (flat `.md` files) | Yes |
| `data-example/` | Example JSON templates for every domain | Yes |
| `data/` | Live user health data | No (gitignored) |
| `data/reference/` | Read-only lookup DBs (food, vaccines, …) | Yes |
| `scripts/` | Python helpers and shell tests | Yes |
| `platform/` | Enterprise FastAPI package | Yes |
| `.claude/` | Runtime workspace (symlinks + local settings) | Partially |
| `Report/` | Generated HTML/Markdown output | No |
| `mydocs/` | Internal roadmap and planning | Mixed |

**Filename = command name.** `commands/allergy.md` → `/allergy`. Use lowercase and hyphens (`mental-health.md` → `/mental-health`).

---

## 5. Extension decision tree

Use this before creating new files:

```
┌─ User needs to record, update, or query health data?
│     └─▶ Command (+ JSON schema in data-example/)
│
├─ User needs deep analysis, trends, or a rich report?
│     └─▶ Skill (command delegates via Skill tool or explicit step)
│
├─ Feature is a clinical opinion in MDT or single-specialty consult?
│     └─▶ Specialist (+ update consult routing rules if new domain)
│
├─ Logic is deterministic, numeric, or too heavy for inline LLM steps?
│     └─▶ Script in scripts/ (+ command invokes via Bash(python3:*))
│
└─ Feature must work via REST API, MCP, or multi-tenant UI?
      └─▶ Platform registration (see Recipe 11) — CLI can ship first
```

**When in doubt:** start with a command for CRUD, extract analysis to a skill when the command file exceeds ~200 lines of analysis logic.

---

## 6. Recipe: Add a command

### When to use

User-facing feature: add/list/update/delete records, run a workflow, or route to a skill.

### Steps

1. **Copy the template**

   ```bash
   cp docs/templates/command.md commands/my-feature.md
   ```

2. **Edit YAML frontmatter** at the top of the file:

   ```yaml
   ---
   description: One-line summary shown in Claude Code command list
   arguments:
     - name: action
       description: "Action type: add/list/analyze/..."
       required: true
     - name: info
       description: Natural language payload (optional)
       required: false
   ---
   ```

3. **Define action types** — one section per action (`add`, `list`, `update`, …) with:
   - Parameter description
   - Usage examples (`/my-feature add …`)
   - Execution steps (numbered instructions for the LLM)

4. **Declare data contracts** — exact paths read/written:

   ```
   Read:  data/my-feature-tracker.json
   Write: data/my-feature-logs/YYYY-MM/YYYY-MM-DD.json
   Update: data/index.json (if indexed)
   ```

5. **Delegate analysis to a skill** when needed:

   ```markdown
   ## Analyze action
   1. Read current data from `data/my-feature-tracker.json`
   2. Invoke the `my-feature-analyzer` skill for deep analysis
   3. Render the skill output using the format below
   ```

6. **Add safety disclaimers** for any clinical or mental-health content (see [§12](#12-safety-and-clinical-modules)).

7. **Add example data** in `data-example/` (see [Recipe 9](#9-recipe-add-a-data-domain)).

8. **Document the command** in [user-guide.md](user-guide.md) (usage examples only — do not duplicate the full command spec).

9. **Validate locally**

   ```bash
   ./scripts/validate-command.sh my-feature
   claude   # test: /my-feature list
   ```

### Checklist

- [ ] File is `commands/<name>.md` (not inside `.claude/`)
- [ ] YAML frontmatter with `description` and `arguments`
- [ ] Every action has examples and execution steps
- [ ] Data paths are explicit (`data/…`, not vague "the tracker file")
- [ ] Analysis delegated to a skill (not embedded in command)
- [ ] Matching template in `data-example/` if the command reads/writes JSON
- [ ] Schema documented in `data-structures.md` if new fields were added
- [ ] Safety disclaimers present for clinical/mental-health modules
- [ ] `user-guide.md` updated with usage examples
- [ ] Platform: added to `AVAILABLE_COMMANDS` if API/MCP access needed (see [Recipe 11](#11-recipe-wire-to-the-platform))

### Reference implementations

| Pattern | Example |
|---------|---------|
| CRUD command | `commands/allergy.md` |
| Multi-action + skill delegation | `commands/nutrition.md` |
| Platform-integrated command | `commands/ai.md` |
| MDT coordinator | `commands/consult.md` |

---

## 7. Recipe: Add a skill

### When to use

Multi-step analysis across many data files, trend detection, correlation analysis, or HTML report generation.

### Steps

1. **Create the skill directory**

   ```bash
   mkdir -p skills/my-feature-analyzer
   cp docs/templates/skill/SKILL.md skills/my-feature-analyzer/SKILL.md
   ```

2. **Edit `SKILL.md` frontmatter**

   ```yaml
   ---
   name: my-feature-analyzer
   description: What this skill analyzes and when to use it
   allowed-tools: Read, Grep, Glob, Write
   ---
   ```

3. **Define skill sections**
   - Features / analysis dimensions
   - Data sources (exact `data/` paths and glob patterns)
   - Step-by-step analysis algorithm
   - Output format (Markdown or HTML template path)
   - Safety boundaries (for health-related skills)

4. **Add supporting files** (optional but recommended for complex skills)

   ```
   skills/my-feature-analyzer/
   ├── SKILL.md
   ├── data-sources.md    # Which files are read and why
   ├── algorithms.md      # Statistical or scoring methods
   ├── examples.md        # Sample inputs/outputs
   └── templates/         # HTML/CSS/JS for reports
   ```

5. **Wire from a command** — add an explicit step in the owning command:

   ```markdown
   2. Invoke Skill("my-feature-analyzer") with the collected data context
   ```

6. **Register in Cursor** (if using Cursor skills) — copy or symlink under `.cursor/skills/` if the skill should appear in Cursor's skill picker. Repo skills in `skills/` are loaded via `.claude/skills` symlink for Claude Code.

### Checklist

- [ ] Directory is `skills/<kebab-name>/SKILL.md`
- [ ] Frontmatter includes `name`, `description`, `allowed-tools`
- [ ] Data sources list exact paths (e.g. `data/nutrition-tracker.json`, `data/nutrition-logs/**/*.json`)
- [ ] Output format is specified (Markdown sections or template file path)
- [ ] No CRUD or user-interaction logic in the skill
- [ ] Safety boundaries documented for clinical analysis
- [ ] Owning command updated to invoke this skill
- [ ] Example output added to `examples.md` for complex skills

### Reference implementations

| Pattern | Example |
|---------|---------|
| Multi-domain analyzer | `skills/nutrition-analyzer/` |
| HTML report + templates | `skills/health-trend-analyzer/` |
| Cross-module correlation | `skills/mental-health-analyzer/` |
| Device import + KB linking | `skills/synapsemd/` |

---

## 8. Recipe: Add a specialist

### When to use

A new medical domain expert for `/consult` (MDT) or `/specialist` (single-specialty consultation).

### Steps

1. **Copy the template**

   ```bash
   cp docs/templates/specialist.md specialists/my-specialty.md
   ```

2. **Fill in required sections**
   - Role definition and areas of expertise
   - Key indicators (labs, imaging) this specialty reviews
   - Analysis principles and framework
   - **Safety red lines** (no dosages, no prescriptions, no prognosis, no diagnosis replacement)
   - Output format (Markdown report sections)
   - Example appropriate vs prohibited phrasing

3. **Update MDT routing** in `commands/consult.md` — add automatic identification rules:

   ```markdown
   - Abnormal <indicator> → My Specialty
   ```

4. **Update `/specialist` command** if the specialty should be directly invokable:

   ```markdown
   /specialist my-specialty [context]
   ```

5. **Verify the specialist is reachable** via symlink:

   ```bash
   ls specialists/my-specialty.md
   ls .claude/specialists/my-specialty.md   # should resolve to same file
   ```

### Checklist

- [ ] File is `specialists/<name>.md` (flat, no subdirectory)
- [ ] Safety red lines section present
- [ ] Output format template defined
- [ ] Appropriate vs prohibited phrasing examples included
- [ ] `commands/consult.md` routing rules updated (if MDT-relevant)
- [ ] `commands/specialist.md` documents the new specialty name (if directly invokable)
- [ ] Specialist receives **summaries**, not raw unfiltered data, in MDT flow

### Reference implementations

| Pattern | Example |
|---------|---------|
| Lab-focused specialty | `specialists/cardiology.md` |
| MDT coordinator | `specialists/consultation-coordinator.md` |

---

## 9. Recipe: Add a data domain

### When to use

A new health tracker, log format, or reference database that commands/skills read and write.

### Steps

1. **Create example template** in `data-example/`:

   ```bash
   cp docs/templates/data-tracker.json data-example/my-feature-tracker.json
   ```

2. **Populate realistic example values** — the example file is the schema contract developers and LLMs rely on.

3. **Add log directory pattern** if the domain uses dated snapshots:

   ```
   data-example/my-feature-logs/
   └── 2025-01/
       └── 2025-01-15.json
   ```

4. **Document the schema** in [data-structures.md](data-structures.md):
   - File path(s)
   - Top-level keys and types
   - Required vs optional fields
   - Relationships to other trackers (e.g. links to `profile.json`)

5. **Update index** if the domain appears in global search — add entry rules to `data-example/index.json` and document in the owning command.

6. **Update setup script** if special seeding is needed:

   ```bash
   # scripts/setup-data.sh — only if non-standard copy/symlink logic is required
   ```

7. **Keep `data/` gitignored** — never commit live user health data. Reference DBs belong in `data/reference/`.

### Data design rules

- **No logic in JSON** — store raw values; compute BMI, scores, and aggregates in commands/skills at runtime.
- **Use consistent date formats** — `YYYY-MM-DD` for dates, `YYYY-MM` for log directory names.
- **Prefer append-only logs** — daily files under `*-logs/YYYY-MM/` for history; tracker file for current state.
- **Reference DBs are read-only** — food, vaccine, and interaction databases live in `data/reference/`.

### Checklist

- [ ] Example file(s) in `data-example/`
- [ ] Schema documented in `data-structures.md`
- [ ] Owning command lists exact read/write paths
- [ ] `data/` remains gitignored; no live PHI committed
- [ ] `./scripts/setup-data.sh` copies new templates (update script if needed)
- [ ] `index.json` updated if globally searchable

---

## 10. Recipe: Add a script

### When to use

Deterministic computation (scoring models, batch report generation), repeated logic shared by CLI and platform, or CI test harnesses.

### Steps

1. **Create the script** in `scripts/`:

   ```bash
   # Python (preferred for shared logic)
   scripts/my_feature_helper.py

   # Shell (integration tests)
   scripts/test-my-feature.sh
   ```

2. **Make platform logic importable** when the script wraps shared code — place reusable modules under `platform/synapsemd_platform/` and keep the script as a thin CLI wrapper (see `scripts/ai_prediction.py` → `AIPredictionEngine`).

3. **Invoke from a command** via whitelisted Bash permission:

   ```markdown
   3. Run: `python3 scripts/my_feature_helper.py --input data/my-feature-tracker.json`
   4. Read the script output and format for the user
   ```

4. **Ensure `.claude/settings.local.json` allows the tool**:

   ```json
   {
     "permissions": {
       "allow": ["Bash(python3:*)", "Bash(node:*)"]
     }
   }
   ```

5. **Add tests** — unit tests in `tests/` for Python modules; shell scripts in `scripts/test-*.sh` for end-to-end command validation.

### Checklist

- [ ] Script lives in `scripts/`, not embedded in markdown
- [ ] Shared logic is importable (not copy-pasted between script and platform)
- [ ] Command documents when and how to invoke the script
- [ ] Bash permission whitelisted if command calls it
- [ ] Tests cover the script or underlying module

### Reference implementations

| Pattern | Example |
|---------|---------|
| Shared engine wrapper | `scripts/ai_prediction.py` |
| Convention validation | `scripts/test-mental-health.sh` |
| Data bootstrap | `scripts/setup-data.sh` |

---

## 11. Recipe: Wire to the platform

### When to use

The command must be executable via REST API (`POST /api/v1/commands/execute`), MCP (`execute_command`), or a chatbot UI — not CLI-only.

**CLI-first is fine.** Skip this recipe until API/MCP access is needed.

### Steps

1. **Register the command** in `platform/synapsemd_platform/api/routes/commands.py`:

   ```python
   AVAILABLE_COMMANDS = [
       "ai", "goal", "consult", ...,
       "my-feature",   # add here
   ]
   ```

2. **Set LLM routing complexity** in `platform/synapsemd_platform/llm/router.py`:

   ```python
   CRITICAL_COMMANDS = {"consult", "specialist", "mental-health", "psych-assess"}
   COMPLEX_COMMANDS = {"report", "ai", "health-trend-analyzer", "interaction", "goal"}
   SIMPLE_COMMANDS = {"profile", "query", "get-profile"}
   ```

   | Command type | Set | Effect |
   |--------------|-----|--------|
   | Clinical / MDT / mental health | `CRITICAL_COMMANDS` | Strongest model + human review |
   | Multi-file analysis, AI, reports | `COMPLEX_COMMANDS` | High-capacity model |
   | Profile, simple queries | `SIMPLE_COMMANDS` | Fast, low-cost model |
   | Everything else | (default) | `MODERATE` |

3. **Special execution path** — only if the command needs structured API beyond generic orchestration (like `/ai`):
   - Add handler in `platform/synapsemd_platform/services/command_orchestrator.py`
   - Add REST routes in `platform/synapsemd_platform/api/routes/`
   - Add MCP tools in `platform/synapsemd_platform/mcp/tools.py` and register in `mcp/dispatch.py`

4. **Document platform usage** — add a "Platform Integration" section to the command markdown (see `commands/ai.md`).

5. **Add tests**
   - Unit: `tests/unit/test_*_routes.py`
   - E2E: `tests/e2e/` for audit trail verification
   - Release: `tests/release/` for PHI/tenant gates if handling sensitive data

6. **Update platform docs** — [platform/README.md](../platform/README.md), [ui-mcp-integration.md](ui-mcp-integration.md).

### Platform execution flow

```
POST /api/v1/commands/execute  { "command": "goal", "context_text": "..." }
        │
        ▼
  CommandOrchestrator
        ├── anonymize context (Presidio)
        ├── route to LLM (HealthLLMRouter)
        ├── apply medical guardrails
        └── emit audit event (hash-only PHI)
```

Generic orchestration reads the command name and anonymized context — it does **not** re-parse `commands/*.md` at runtime. Keep command markdown as the spec for LLM agents; platform routes add auth, tenancy, and safety.

### Checklist

- [ ] Command added to `AVAILABLE_COMMANDS`
- [ ] Complexity set in `HealthLLMRouter` (`CRITICAL` / `COMPLEX` / `SIMPLE`)
- [ ] Dedicated REST/MCP handlers added if generic orchestration is insufficient
- [ ] "Platform Integration" section in command markdown
- [ ] Tests added (unit + e2e where audit/PHI applies)
- [ ] Platform docs updated

### Module 21 AI reference

| CLI | REST | MCP |
|-----|------|-----|
| `/ai status` | `GET /api/v1/ai/status` | `ai_status` |
| `/ai analyze` | `POST /api/v1/ai/analyze` | `ai_analyze` |
| `/ai predict` | `POST /api/v1/ai/predict` | `ai_predict` |
| `/ai chat` | `POST /api/v1/ai/chat` | `ai_chat` |
| `/ai report` | `POST /api/v1/ai/report` | `ai_report` |

Engine: `platform/synapsemd_platform/ai/prediction.py` (`AIPredictionEngine`).

---

## 12. Safety and clinical modules

Any command, skill, or specialist that touches diagnosis, treatment, mental health, or medication must include **safety boundaries**.

### Required disclaimers (clinical modules)

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis
5. Output is for reference only — consult a qualified professional

### Mental-health additions

- Does not perform psychological diagnosis
- Does not prescribe psychiatric medication
- Does not predict suicide risk as a definitive assessment
- Crisis resources and escalation paths for self-harm indicators

### Where to put disclaimers

| Artifact | Location |
|----------|----------|
| Command | Top of file or dedicated "Safety" section + per-action reminders |
| Skill | "Medical safety boundaries" section in `SKILL.md` |
| Specialist | "Safety red lines" section with prohibited phrasing examples |

Reference: [safety-guidelines.md](safety-guidelines.md), [clinical-safety-policy.md](clinical-safety-policy.md).

Validate conventions:

```bash
./scripts/test-mental-health.sh    # example pattern for clinical modules
```

---

## 13. Testing your extension

### Local CLI smoke test

```bash
./scripts/setup-data.sh
claude
# Run your new command interactively
```

### Automated tests

```bash
pytest -v                                    # full platform suite (266+ tests)
pytest tests/unit/ -v                        # unit tests only
pytest tests/release/ tests/eval/ -v         # release gates + model eval
./scripts/validate-command.sh my-feature   # command structure lint
./scripts/test-my-feature.sh                 # optional domain-specific script
```

### Coverage policy

Platform code (`synapsemd_platform`) enforces **≥95% coverage** in CI. New platform handlers need tests in `tests/unit/` or `tests/integration/`.

### PR checklist

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full contribution checklist.

---

## 14. Documentation map

| You changed… | Update… |
|--------------|---------|
| New command usage | [user-guide.md](user-guide.md) |
| New JSON schema | [data-structures.md](data-structures.md) |
| Architecture / deployment | [architecture.md](architecture.md) |
| Platform API / MCP | [platform/README.md](../platform/README.md), [ui-mcp-integration.md](ui-mcp-integration.md) |
| Release / compliance impact | [release-gates.md](release-gates.md) |
| Extension conventions | This guide ([developer-guide.md](developer-guide.md)) |

**Do not duplicate** full command specs in the user guide — link to `commands/<name>.md` or show short examples only.

---

## 15. Common mistakes

| Mistake | Fix |
|---------|-----|
| Editing `.claude/commands/` directly | Edit `commands/` at repo root; verify symlinks |
| Copying commands/skills instead of symlinking | Run `./scripts/link-claude-workspace.sh` |
| Putting analysis logic in commands | Extract to `skills/<name>/SKILL.md` |
| Putting CRUD in skills | Move to command; skill reads data command prepared |
| New JSON shape without `data-example/` template | Add template + document in `data-structures.md` |
| Computed fields stored in JSON | Compute at runtime in command/skill |
| Clinical module without disclaimers | Add safety section; run validation script |
| CLI command without platform registration | Add to `AVAILABLE_COMMANDS` when API access needed |
| Committing `data/` live files | Only commit `data-example/` and `data/reference/` |
| Specialist reads raw lab dumps in MDT | Pass summarized context from consult coordinator |

---

## Quick links

- [Architecture](architecture.md)
- [Data structures](data-structures.md)
- [User guide](user-guide.md)
- [Platform README](../platform/README.md)
- [MCP / UI integration](ui-mcp-integration.md)
- [Release gates](release-gates.md)
- [Contributing](../CONTRIBUTING.md)
- [Templates](templates/)
