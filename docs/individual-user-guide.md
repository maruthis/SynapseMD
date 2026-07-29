# SynapseMD for Individual Users

**Audience:** Developers using SynapseMD on a personal machine, and clinicians using it as a **personal health assistant** via an IDE (Cursor / Claude Code), **Open WebUI**, or **AnythingLLM**.

This document covers **architecture, features, commands, and usage** for single-user / personal workflows only. It does **not** cover multi-tenant enterprise ops, Kubernetes production hardening, or BAA/compliance program management.

| Related docs | Purpose |
|--------------|---------|
| [getting-started.md](getting-started.md) | Step-by-step first setup |
| [commands-catalog.md](commands-catalog.md) | Full command reference |
| [architecture.md](architecture.md) | Full system architecture (including enterprise) |
| [anythingllm-setup.md](anythingllm-setup.md) | AnythingLLM + MCP |
| [open-webui-setup.md](open-webui-setup.md) | Open WebUI v0.10.2 |
| [developer-guide.md](developer-guide.md) | Extending commands / skills / specialists |
| [sme-guide-add-command-skill-specialist.md](sme-guide-add-command-skill-specialist.md) | SME walkthrough: add command + skill + specialist (gout / rheumatology example) |

**GitHub:** [https://github.com/maruthis/SynapseMD](https://github.com/maruthis/SynapseMD)

---

## Table of contents

1. [Who this is for](#1-who-this-is-for)
2. [Architecture (individual use)](#2-architecture-individual-use)
3. [Features](#3-features)
4. [Two personas](#4-two-personas)
5. [Setup paths](#5-setup-paths)
6. [Commands and usage](#6-commands-and-usage)
7. [Typical workflows](#7-typical-workflows)
8. [Safety and privacy](#8-safety-and-privacy)
9. [Where to go next](#9-where-to-go-next)

---

## 1. Who this is for

| Persona | Goal | Primary interface |
|---------|------|-------------------|
| **Developer (personal)** | Private health vault on disk; scriptable, versionable, extendable | Cursor / Claude Code slash commands over `data/` |
| **Doctor’s personal assistant** | Visit prep, labs briefing, MDT-style synthesis for *one* practice / one machine | IDE **or** chat UI (Open WebUI / AnythingLLM) via local MCP |

**Out of scope for this guide:** hospital-wide multi-tenant SaaS, shared EHR certification, production K8s fleets.

---

## 2. Architecture (individual use)

### 2.1 Core idea

SynapseMD is artifact-driven:

| Layer | Folder | Role |
|-------|--------|------|
| **Commands** | `commands/*.md` | What the user types (`/profile`, `/consult`, …) |
| **Skills** | `skills/*/SKILL.md` | Deep analysis recipes |
| **Specialists** | `specialists/*.md` | Clinical lenses for `/consult` / `/specialist` |
| **Data vault** | `data/` | Your JSON records (gitignored) |
| **Templates** | `data-example/` | Schemas copied by setup |
| **Optional platform** | `platform/` | Local FastAPI + MCP so chat UIs can call tools |

### 2.2 Path A — IDE only (no Docker required)

Best for developers and clinicians comfortable in Cursor / Claude Code.

```text
You
  → Cursor / Claude Code
       → loads commands/ + skills/ + specialists/ (via .claude/ symlinks)
       → reads/writes data/*.json
       → optional scripts (e.g. Module 21 ai_prediction)
```

- No database.
- Agent follows markdown playbooks.
- Skills and specialist fan-out happen in the IDE (e.g. `/consult` launches specialty Tasks).

### 2.3 Path B — Local platform + chat UI (doctor assistant / chat UX)

Best when you want a browser chat shell (Open WebUI or AnythingLLM) instead of slash commands.

```text
You (browser)
  → Open WebUI (:3000)  or  AnythingLLM (:3001 / Desktop)
       → SynapseMD MCP SSE (:8081/sse)
            → Platform API (:8000)
                 → JWT auth (single tenant/user for personal use)
                 → AI tools / command execute
                 → local data / FHIR store (Compose stack)
```

Open WebUI / AnythingLLM are **thin chat UIs**. They must **not** become the system of record for labs or PHI dumps in prompts.

### 2.4 How a command runs (IDE)

```text
/save-report path.pdf
    → Agent loads commands/save-report.md
    → Extracts structured values
    → Writes data/biochemical-tests/… or imaging-examinations/…
    → Updates data/index.json
```

```text
/consult recent 3
    → commands/consult.md
    → Parallel specialists/*.md
    → consultation-coordinator.md merges MDT report
```

```text
/ai predict diabetes
    → commands/ai.md
    → Module 21 AIPredictionEngine (local / platform shared logic)
```

Full sequence diagrams: [architecture.md §6.3](architecture.md#63-ide--cli--providing-and-invoking-commands-skills-specialists) (command · skill · specialist on IDE/CLI).

---

## 3. Features

### Personal vault

- File-based JSON under `data/` — private by default
- Lab / imaging ingest from PDF or image (`/save-report`)
- Index and query (`/query`)
- Profile, allergies, meds, vaccines, surgery, radiation, symptoms, family history

### Clinical decision *support* (not diagnosis)

- Multidisciplinary `/consult` and single-specialty `/specialist`
- Visit prep (`/prepare`)
- Drug interaction checks (`/interaction`, `/polypharmacy`)
- Chronic disease trackers (hypertension, diabetes, COPD, …)

### Lifestyle and goals

- Sleep, fitness, nutrition, diet, goals / habits
- Women’s, men’s, child, mental health, specialty body systems, travel, TCM, and more

### AI (Module 21)

| Action | What it does |
|--------|----------------|
| `/ai analyze` | Multi-source analysis over your vault |
| `/ai predict <risk>` | Hypertension, diabetes, CVD, nutrition, sleep (simplified models) |
| `/ai chat …` | Natural-language Q&A over local data |
| `/ai report generate` | HTML / structured report |
| `/ai status` | Feature flags and config |

### Chat UI access (optional)

- **AnythingLLM** → MCP SSE tools
- **Open WebUI** → Workspace Tools (OpenAPI bridge) and/or MCP SSE

---

## 4. Two personas

### 4.1 Developer (personal machine)

**Use when:** You want full control, markdown extensibility, and local privacy.

1. Clone repo → `./scripts/setup-data.sh` → `./scripts/link-claude-workspace.sh`
2. Open folder in **Cursor** or **Claude Code**
3. Use slash commands against `data/`
4. Extend by adding `commands/*.md`, `skills/*/SKILL.md`, or `specialists/*.md` (see [developer-guide.md](developer-guide.md))

**Typical day:**

```bash
/profile set M 175 70 1990-01-01
/save-report ~/Downloads/lab.pdf
/query recent 5
/ai analyze last_quarter
/consult recent 3
```

### 4.2 Personal assistant for a doctor

**Use when:** A clinician wants briefing, synthesis, and prep on a **dedicated machine** (single user / single practice vault).

| Interface | When to prefer it |
|-----------|-------------------|
| **IDE** | Fastest fidelity: full `/consult` specialist fan-out, `/prepare`, report save |
| **AnythingLLM** | Familiar chat UX; MCP tools for AI status / predict / analyze / chat / report |
| **Open WebUI** | Browser-based tools via bridge or MCP; good for non-IDE staff |

**Recommended clinical habits:**

1. One vault per patient *or* clear identity discipline when ingesting labs (mismatched PDF names break analysis).
2. Prefer `/prepare Cardiology` and `/consult` / `/specialist` in IDE for MDT-quality output.
3. Keep chat UIs thin — authenticate MCP with a SynapseMD JWT; do not paste full PHI into system prompts.
4. Always treat outputs as **decision support**, not diagnosis or prescribing.

---

## 5. Setup paths

### 5.1 IDE (developer or doctor) — minimum path

```bash
git clone https://github.com/maruthis/SynapseMD.git
cd SynapseMD
./scripts/setup-data.sh
./scripts/link-claude-workspace.sh
```

Open the repo in Cursor or Claude Code, then:

```text
/profile set M 175 70 1990-01-01
/profile view
```

Details: [getting-started.md](getting-started.md).

### 5.2 Local platform for chat UIs

```bash
cd platform
cp .env.example .env   # set secrets / LLM provider as needed
docker compose --profile full up --build -d
```

Useful endpoints for personal use:

| Service | URL |
|---------|-----|
| API health | http://localhost:8000/health |
| MCP health | http://localhost:8081/health |
| MCP SSE | http://localhost:8081/sse |
| Open WebUI (Compose) | http://localhost:3000 |
| AnythingLLM (Compose) | http://localhost:3001 |

Create/login a user via `POST /api/v1/auth/login`, put the `access_token` in `platform/.env` as `SYNAPSEMD_ACCESS_TOKEN`, recreate MCP:

```bash
docker compose --profile mcp up -d mcp
```

### 5.3 AnythingLLM (personal)

- Point MCP at `http://localhost:8081/sse` (Desktop) or `http://mcp:8081/sse` (Compose network).
- Token lives in **`platform/.env`**, not in AnythingLLM, for Docker MCP paths.

Full steps: [anythingllm-setup.md](anythingllm-setup.md).

### 5.4 Open WebUI v0.10.2 (personal)

- Prefer **Workspace → Tools** via OpenAPI bridge (`:8100`), or MCP SSE `:8081/sse`.
- Use a tool-calling chat model.

Full steps: [open-webui-setup.md](open-webui-setup.md).

---

## 6. Commands and usage

**Total: 59 slash commands** (source: `commands/`).  
Full table: [commands-catalog.md](commands-catalog.md). Definitions: `commands/<name>.md`.

### How to read usage

- `a/b/c` — alternative subcommands  
- `<required>` · `[optional]` · `…` free text  

### 6.1 Everyday essentials

| Command | Usage | Notes |
|---------|-------|-------|
| `/profile` | `set <H_cm> <W_kg> <YYYY-MM-DD>` · `view` · `<field>=<value>` | Start here |
| `/get-profile` | *(no args)* | Visual profile |
| `/save-report` | `<image_or_pdf_path> [exam_date]` | Labs / imaging ingest |
| `/query` | `all` · `biochemical` · `imaging` · `abnormal` · `recent [N]` · `date <d>` | Browse vault |
| `/prepare` | `[department…]` | Visit briefing |
| `/allergy` | `add/list/update/delete [info…]` | Allergy list |
| `/medication` | `add/log/list/history/status [info…]` | Meds |
| `/interaction` | `check/list/… [drugs…]` | Interaction check |
| `/consult` | `all` · `recent [N]` · `date …` · *(default recent 3)* | MDT synthesis |
| `/specialist` | `list` · `<specialty> [params…]` | One specialty |
| `/ai` | `analyze` · `predict <risk>` · `chat …` · `report generate` · `status` | Module 21 |
| `/report` | `comprehensive/biochemical/…` | HTML reports |

### 6.2 By category (summary)

**Patient info & history:** `/profile`, `/get-profile`, `/prepare`, `/surgery`, `/discharge`, `/vaccine`, `/family`, `/symptom`, `/radiation`, `/radiation-data`

**Allergies & meds:** `/allergy`, `/medication`, `/interaction`, `/polypharmacy`

**Labs & imaging:** `/save-report`, `/query`, `/screening`

**Lifestyle:** `/sleep`, `/fitness`, `/nutrition`, `/diet`, `/goal`

**Chronic disease:** `/hypertension`, `/diabetes`, `/copd`

**Women’s health:** `/cycle`, `/pregnancy`, `/postpartum`, `/menopause`

**Men’s health:** `/prostate-health`, `/male-fertility`, `/male-menopause`

**Child & adolescent:** `/child-development`, `/child-illness`, `/child-mental`, `/child-nutrition`, `/child-safety`, `/child-sleep`, `/child-vaccine`, `/growth`, `/puberty`

**Mental health:** `/mental-health`, `/psych-assess`, `/mood`, `/cognitive`

**Specialty systems & rehab:** `/eye-health`, `/oral-health`, `/skin-health`, `/sexual-health`, `/rehabilitation`, `/fall`

**Occupational / travel / TCM:** `/occupational-health`, `/travel-health`, `/tcm-constitution`

**Consultation & AI:** `/consult`, `/specialist`, `/ai`, `/report`, `/report-instructions`

### 6.3 AI usage cheatsheet

```text
/ai status
/ai analyze last_quarter
/ai predict diabetes
/ai predict hypertension
/ai predict all
/ai chat How has my fasting glucose changed?
/ai report generate comprehensive
```

Supported predict types: `hypertension` · `diabetes` · `cardiovascular` · `nutritional_deficiency` · `sleep_disorder` · `all`

### 6.4 Chat UI mapping (personal platform)

When MCP is connected, prefer tools such as:

| MCP / API style | Rough CLI equivalent |
|-----------------|----------------------|
| `ai_status` | `/ai status` |
| `ai_analyze` | `/ai analyze` |
| `ai_predict` | `/ai predict` |
| `ai_chat` | `/ai chat` |
| `ai_report` | `/ai report generate` |

IDE still gives the richest `/consult` and `/save-report` experience today.

---

## 7. Typical workflows

### Developer — weekend personal vault

1. Setup + `/profile set …`
2. `/save-report` for labs
3. `/query abnormal`
4. `/ai predict diabetes` / `/ai analyze`
5. Optionally extend a skill in `skills/`

### Doctor — visit prep (IDE)

1. Ensure the correct patient vault / identity on reports
2. `/query recent 5`
3. `/prepare Cardiology` (or department)
4. `/consult recent 5` or `/specialist cardiology`
5. Share **synthesized briefing** with the clinician; clinician owns diagnosis

### Doctor — chat assistant (AnythingLLM / Open WebUI)

1. Start Compose `full` or `mcp` profile
2. Connect SSE MCP; set JWT in `platform/.env`
3. Ask: “Summarize latest labs” / “Run diabetes risk prediction” via tools
4. For MDT-depth consults, switch to IDE `/consult`

---

## 8. Safety and privacy

- **Not a physician.** Outputs are informational decision support.
- **No prescribing / no dosages / no mortality prognosis** in specialist flows.
- **Local-first:** personal `data/` stays on disk; chat UIs should not store the clinical graph.
- **Identity:** do not merge lab PDFs from different patients into one vault without labeling.
- **Emergencies:** call emergency services — do not rely on SynapseMD.

---

## 9. Where to go next

| Need | Doc |
|------|-----|
| First-time setup | [getting-started.md](getting-started.md) |
| Every command | [commands-catalog.md](commands-catalog.md) |
| Deeper architecture / flows | [architecture.md](architecture.md) |
| AnythingLLM | [anythingllm-setup.md](anythingllm-setup.md) |
| Open WebUI | [open-webui-setup.md](open-webui-setup.md) |
| Add a command/skill/specialist | [developer-guide.md](developer-guide.md) · SME walkthrough: [sme-guide-add-command-skill-specialist.md](sme-guide-add-command-skill-specialist.md) |
| Platform API details | [../platform/README.md](../platform/README.md) |

---

*SynapseMD — individual / personal-assistant usage guide. Independent open-source project.*
