# SME Guide: Add a Command, Skill, and Specialist

**Audience:** Subject-matter experts (SMEs), clinicians, and clinical informatics leads who want to extend SynapseMD **without writing application code**.  
**Companion (engineer detail):** [developer-guide.md](developer-guide.md) · Templates: [docs/templates/](templates/) · Runtime flows: [architecture.md §6.3](architecture.md#63-ide--cli--providing-and-invoking-commands-skills-specialists)

---

## 1. What you are adding (plain language)

SynapseMD is driven by **markdown playbooks**. You place files in the repo; Cursor / Claude Code discovers them via `.claude/` symlinks. No compile step for local IDE/CLI use.

| You create… | Folder | What the clinician/user experiences |
|-------------|--------|-------------------------------------|
| **Command** | `commands/<name>.md` | A slash command such as `/gout add …` — log and list records |
| **Skill** | `skills/<name>/SKILL.md` | Deeper pattern analysis when the command says “analyze” |
| **Specialist** | `specialists/<name>.md` | A clinical lens for `/specialist …` or multidisciplinary `/consult` |

```text
Who does what?
  Command  →  “front desk + charting”   (capture / list / update data)
  Skill    →  “analyst”                 (trends, correlations, report)
  Specialist → “consulting physician”   (interpret findings in one specialty voice)
```

---

## 2. Worked example: Gout flare diary + Rheumatology lens

### Clinical story

Dr. Rao (rheumatology) wants SynapseMD to:

1. Let a user **log gout flares** in everyday language (`/gout add …`).
2. Run a **pattern review** (frequency, triggers, uric-acid notes) via a skill.
3. Include a **Rheumatology** opinion in `/consult` and allow `/specialist rheum …`.

This example is a **tutorial**. Copy the snippets into the folders below to make the feature live in your workspace. It is **not** a substitute for diagnosis, prescribing, or formal clinical validation.

### Safety red lines (every clinical artifact)

1. Do **not** provide specific medication dosages.  
2. Do **not** prescribe drug names as orders.  
3. Do **not** give life-or-death prognoses.  
4. Do **not** replace a physician’s diagnosis.  

Output is for personal health reference and care-team discussion only.

---

## 3. Where files go in the project

Edit files under the **repo root** folders — never create permanent copies only under `.claude/` (those are symlinks).

```text
SynapseMD/
├── commands/
│   └── gout.md                          ← NEW command (slash /gout)
├── skills/
│   └── gout-analyzer/
│       └── SKILL.md                     ← NEW skill
├── specialists/
│   └── rheumatology.md                  ← NEW specialist
├── data-example/
│   └── gout-tracker.json                ← NEW example schema (recommended)
├── data/                                ← live vault (gitignored; created on use)
│   └── gout-tracker.json
├── .claude/
│   ├── commands      → ../commands      (symlink — do not edit as the source of truth)
│   ├── skills        → ../skills
│   └── specialists   → ../specialists
└── docs/templates/                      ← blank starters you can copy
```

If symlinks are missing:

```bash
./scripts/link-claude-workspace.sh
ls -la .claude/commands .claude/skills .claude/specialists
```

---

## 4. Step A — Create the Command (`/gout`)

### 4.1 Copy the template

```bash
cp docs/templates/command.md commands/gout.md
```

### 4.2 Replace with a clinician-readable playbook

Save as `commands/gout.md` (abbreviated but complete enough to run):

```markdown
---
description: Log and review gout flare episodes (joint, severity, triggers)
arguments:
  - name: action
    description: "Action type: add/list/update/analyze"
    required: true
  - name: info
    description: Natural language flare details or filter
    required: false
---

# Gout Flare Diary

Personal tracker for gout flares — joint involved, severity, possible triggers, and notes.
Supports quick logging and pattern analysis (via skill). For reference only; not a diagnosis.

## Action Types

### 1. Add flare — `add`

**Examples:**
```
/gout add right big toe severe overnight after seafood and beer
/gout add left ankle moderate after long walk uric acid last checked 7.8
```

### 2. List flares — `list`

**Examples:**
```
/gout list
/gout list severe
/gout list last 90 days
```

### 3. Update flare — `update`

**Examples:**
```
/gout update right big toe status resolving
/gout update left ankle notes ice helped overnight
```

### 4. Analyze patterns — `analyze`

Delegates deep analysis to the skill (do not embed scoring algorithms here).

**Examples:**
```
/gout analyze
/gout analyze last 6 months
```

## Data Contract

| Operation | Path |
|-----------|------|
| Read/Write | `data/gout-tracker.json` |
| Example schema | `data-example/gout-tracker.json` |

## Execution Steps

### Add

1. Parse `info` into fields: `joint`, `side`, `severity` (mild/moderate/severe), `triggers[]`, `notes`, optional `uric_acid_mg_dl`, `onset` (ISO date if stated, else today).
2. Read `data/gout-tracker.json` (create from `data-example/gout-tracker.json` structure if missing).
3. Append a record with unique `id` and `recorded_at` (ISO timestamp).
4. Write the file back.
5. Confirm using the output format below.

### List

1. Read `data/gout-tracker.json`.
2. Filter by keywords in `info` if provided (`severe`, joint name, date window).
3. Render a concise table/list.

### Analyze

1. Read `data/gout-tracker.json`.
2. Invoke Skill("gout-analyzer") with the tracker content and any date window from `info`.
3. Present the skill report to the user with disclaimers.

## Output Format

```markdown
## Gout Diary — [Action]

- **Summary**: …
- **Latest / matching flares**: …
- **Next step suggestion**: lifestyle monitoring or clinician follow-up (non-prescriptive)
```

## Safety

This command is for personal health management only. It:

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis

All output is for reference only. Consult a qualified healthcare professional for medical decisions.
```

### 4.3 Add an example data file (recommended)

```bash
cp docs/templates/data-tracker.json data-example/gout-tracker.json
```

Example content for `data-example/gout-tracker.json`:

```json
{
  "version": "1.0",
  "flares": [
    {
      "id": "gout-2026-07-01-001",
      "recorded_at": "2026-07-01T08:30:00+05:30",
      "onset": "2026-07-01",
      "joint": "first MTP",
      "side": "right",
      "severity": "severe",
      "triggers": ["seafood", "alcohol"],
      "uric_acid_mg_dl": 7.8,
      "status": "active",
      "notes": "Woke with pain; difficulty walking"
    }
  ]
}
```

After first real use, the live file will be `data/gout-tracker.json` (usually gitignored).

### 4.4 Validate the command shell

```bash
./scripts/validate-command.sh gout
```

Reload the IDE / Claude Code session, then try:

```text
/gout add right big toe severe after seafood
/gout list
```

**You should see:** a confirmation that a flare was written under `data/gout-tracker.json`.

---

## 5. Step B — Create the Skill (`gout-analyzer`)

### 5.1 Create the skill folder

```bash
mkdir -p skills/gout-analyzer
cp docs/templates/skill/SKILL.md skills/gout-analyzer/SKILL.md
```

### 5.2 Skill playbook

Save as `skills/gout-analyzer/SKILL.md`:

```markdown
---
name: gout-analyzer
description: Analyze gout flare diary for frequency, triggers, severity trends, and monitoring suggestions.
allowed-tools: Read, Grep, Glob, Write
---

# Gout Analyzer Skill

Analyze `data/gout-tracker.json` (and optional related labs/nutrition notes) to surface patterns for discussion with a clinician.

## Features

### 1. Flare frequency and severity

- Count flares in the requested window (default: last 6 months)
- Severity mix (mild / moderate / severe)
- Joints most often involved

### 2. Trigger signals

- Recurring dietary or lifestyle triggers mentioned in notes
- Cluster detection (multiple flares within 14 days)

### 3. Cross-checks (if files exist)

| Domain | Path | Why |
|--------|------|-----|
| Profile | `data/profile.json` | Age/sex context only |
| Nutrition | `data/nutrition-tracker.json` | Optional diet context |
| Labs (if saved) | exam / report JSON under `data/` | Uric acid mentions if present |

## Analysis Steps

1. Load `data/gout-tracker.json` via Read (Glob if path uncertain).
2. Filter by date window from the invoking command.
3. Aggregate frequency, severity, joints, and trigger keywords.
4. Note missing data (e.g. no uric acid values) without inventing numbers.
5. Produce the report format below.
6. Stay within medical safety boundaries.

## Output Format

```markdown
## Gout Pattern Analysis

### Summary
- Window: …
- Flare count: …
- Predominant joints / severity: …

### Possible trigger patterns
- … (observational; not proven causation)

### Monitoring suggestions (non-prescriptive)
- What to log next time
- When to discuss with a clinician (e.g. increasing frequency or new joints)

### Disclaimer
Personal reference only — not a diagnosis or treatment plan.
```

## Medical Safety Boundaries

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis

Output is for reference only.
```

The `/gout analyze` steps in the command already call `Skill("gout-analyzer")`. After reload:

```text
/gout analyze last 6 months
```

**You should see:** a pattern report grounded in the diary file (and a clear disclaimer).

---

## 6. Step C — Create the Specialist (`rheumatology`)

### 6.1 Copy the template

```bash
cp docs/templates/specialist.md specialists/rheumatology.md
```

### 6.2 Specialist lens

Save as `specialists/rheumatology.md`:

```markdown
# Rheumatology Specialist Skill

## Role Definition

You are an experienced **Rheumatology** specialist focused on crystal arthropathy, inflammatory joint disease signals, and musculoskeletal laboratory/clinical pattern review for **educational and care-coordination** purposes.

## Areas of Expertise

- Gout and hyperuricemia-related flare patterns
- Inflammatory vs mechanical joint pain clues (from documented data only)
- Basic rheumatologic lab context (e.g. uric acid, CRP/ESR **if present in the record**)
- Lifestyle factors commonly discussed in gout education (diet, alcohol, hydration) — non-prescriptive

## Analysis Focus

### Key indicators (when available in supplied data)

- **Labs**: serum uric acid, CRP, ESR, CBC if present
- **Diary**: flare joint, severity, frequency, triggers
- **Comorbid context**: CKD, diuretic exposure, metabolic syndrome **only if documented**

## Analysis Principles

### Safety Red Lines (Strictly Observed)

1. **Do not provide specific medication dosages**
2. **Do not directly prescribe medication names**
3. **Do not make life-or-death prognoses**
4. **Do not replace physician diagnosis**

### Analysis Framework

1. Summarize documented flares and labs
2. Flag out-of-range values only when reference context is present
3. Comment on pattern concerns (e.g. accelerating flare rate)
4. Suggest non-prescriptive lifestyle discussion points
5. Recommend when in-person rheumatology / primary-care review is appropriate

## Output Format

```markdown
## Rheumatology Analysis Report

### Data Overview
- Key findings from diary / labs: …

### Detailed Analysis
1. **Flare pattern** — …
2. **Lab context** — … (or “not available in supplied data”)

### Recommendations
- Lifestyle discussion points: …
- Medical advice: whether clinician follow-up is suggested (no prescriptions)

### Disclaimer
Reference only — does not replace clinical assessment.
```

## Example Phrasing

### Appropriate

- "Documented flares involve the first MTP with dietary triggers noted; discuss pattern and monitoring plan with a clinician."
- "Uric acid value in the record is above common reference ranges if those ranges were supplied; confirm with the treating clinician."

### Prohibited

- "Start allopurinol 300 mg daily" (dose / prescription)
- "Confirmed chronic tophaceous gout" (replacing diagnosis)
- "Risk of renal failure and early death" (prognosis)

## Analysis Requirements

- Stay within the data provided
- Separate observation from diagnosis
- Always include a reference-only disclaimer
```

### 6.3 Wire into `/specialist` and `/consult`

**A. Direct specialty code** — edit `commands/specialist.md` and add a row (and matching code), for example:

| Specialty code | Specialty name | File | Area of expertise |
|----------------|----------------|------|-------------------|
| `rheum` | Rheumatology | `rheumatology.md` | Gout, inflammatory arthritis signals |

Usage after wiring:

```text
/specialist rheum recent 5
/specialist list
```

**B. MDT auto-routing** — edit `commands/consult.md` “Automatic identification rules”, for example:

```markdown
- Recurrent monoarticular flares, elevated uric acid, or gout diary signals → Rheumatology
```

Then:

```text
/consult recent 5
```

When gout/uric-acid signals are present, the main agent should launch a **Task subagent** using `specialists/rheumatology.md` (see [architecture.md §6.3](architecture.md#63-ide--cli--providing-and-invoking-commands-skills-specialists)).

---

## 7. End-to-end checklist (SME)

Do these in order:

| # | Action | Done when… |
|---|--------|------------|
| 1 | Add `commands/gout.md` | `/gout` appears after IDE/CLI reload |
| 2 | Add `data-example/gout-tracker.json` | Schema exists for the agent to copy |
| 3 | Run `./scripts/validate-command.sh gout` | Script exits successfully |
| 4 | `/gout add …` then `/gout list` | `data/gout-tracker.json` updates |
| 5 | Add `skills/gout-analyzer/SKILL.md` | `/gout analyze` returns a pattern report |
| 6 | Add `specialists/rheumatology.md` | File visible via `.claude/specialists/` |
| 7 | Update `commands/specialist.md` + `commands/consult.md` | `/specialist rheum` and MDT routing work |
| 8 | Repair symlinks if needed | `./scripts/link-claude-workspace.sh` |
| 9 | Keep safety red lines in all three artifacts | No dosing / prescribing / prognosis / fake diagnosis |

Optional engineer follow-ups (not required for local IDE use):

- Document schema in [data-structures.md](data-structures.md)
- Add a short usage line to [user-guide.md](user-guide.md) / [commands-catalog.md](commands-catalog.md)
- Register the command for API/MCP in the platform (`AVAILABLE_COMMANDS`) — see [developer-guide.md §11](developer-guide.md#11-recipe-wire-to-the-platform)

---

## 8. How you know “functionality is available”

| Test | Expected behavior |
|------|-------------------|
| `/gout add right knee moderate after beer` | Main agent follows `commands/gout.md`, writes JSON, confirms |
| `/gout list` | Lists flares from `data/gout-tracker.json` |
| `/gout analyze` | Main agent loads Skill `gout-analyzer`, reads diary, returns pattern report |
| `/specialist rheum recent 3` | Main agent spawns one Task subagent with `rheumatology.md` |
| `/consult recent 5` (with gout/uric signals) | Rheumatology included among parallel specialist Tasks |

Under the hood (IDE/CLI): **Host → Main agent + Main LLM → tools**; skills stay on the main agent; specialists use **Task subagent(s) + Subagent LLM(s)**. Details: [architecture.md §6.3](architecture.md#63-ide--cli--providing-and-invoking-commands-skills-specialists).

---

## 9. Choosing your own clinical topic

Use the same three-file pattern for any domain:

| If the SME wants… | Create… | Example slash |
|-------------------|---------|---------------|
| Structured logging | Command + `data-example` tracker | `/migraine`, `/peak-flow` |
| Trends / correlation | Skill invoked from `analyze` | `migraine-analyzer` |
| Specialty voice in MDT | Specialist + consult/specialist wiring | `/specialist ent` |

Prefer **one command ↔ one skill ↔ one specialty** for the first vertical. Expand only after the diary + analyze path works end-to-end.

---

## 10. Related docs

| Doc | Use when |
|-----|----------|
| [docs/templates/command.md](templates/command.md) | Blank command starter |
| [docs/templates/skill/SKILL.md](templates/skill/SKILL.md) | Blank skill starter |
| [docs/templates/specialist.md](templates/specialist.md) | Blank specialist starter |
| [developer-guide.md](developer-guide.md) | Full checklists, platform wiring, common mistakes |
| [clinical-safety-policy.md](clinical-safety-policy.md) | Safety expectations |
| [individual-user-guide.md](individual-user-guide.md) | How clinicians use SynapseMD day to day |

---

*This guide teaches SMEs how to author playbooks. Formal clinical validation, governance sign-off, and production platform registration remain organizational responsibilities.*
