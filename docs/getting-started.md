# Getting Started with SynapseMD

This guide is for **end users** — people who want to manage their personal health data with SynapseMD, not developers extending the codebase.

If you want to add commands, skills, or platform features, see the [Developer Guide](developer-guide.md) instead.

---

## What SynapseMD gives you

SynapseMD is a **private, file-based health record** on your computer. You interact with it through natural language and slash commands in [Claude Code](https://claude.ai/code) or [Cursor](https://cursor.com/) — no web account, no cloud database, no app store install.

You can:

- Save lab reports and imaging results from photos or files
- Track medications, allergies, surgeries, radiation exposure, and dozens of other health domains
- Query your records in plain language
- Run AI analysis and risk predictions on your own data
- Get multi-specialty consultation-style reports (for reference only — not a diagnosis)

**All your health data stays in a local `data/` folder on your machine.**

---

## What you need before you start

| Requirement | Details |
|-------------|---------|
| **Computer** | macOS, Linux, or Windows with WSL |
| **Git** | To clone the repository |
| **Claude Code or Cursor** | To run slash commands against your repo |
| **Anthropic API access** | Claude Code/Cursor uses Claude models (API usage may incur cost) |
| **Optional** | Python 3.11+ only if you use the enterprise platform locally |

You do **not** need to know programming. You only need to type commands like `/profile set 175 70 1990-01-01`.

---

## Step 1 — Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/maruthis/SynapseMD.git
cd SynapseMD
```

This creates a folder on your computer containing all command definitions and empty data templates. Your personal health records will live inside this folder under `data/`.

---

## Step 2 — Initialize your personal data folder

Run the setup script once:

```bash
./scripts/setup-data.sh
```

This script:

1. Creates `data/` if it does not exist
2. Copies example tracker templates from `data-example/` into `data/` (only on first run)
3. Links reference databases (food, vaccines, etc.)
4. Seeds `data/ai-config.json` for AI features

**Safe to re-run.** If you already have `data/profile.json`, the script skips copying templates so it will not overwrite your records.

Verify it worked:

```bash
ls data/profile.json data/allergies.json
```

You should see JSON files — these are your empty trackers ready to fill in.

---

## Step 3 — Link the Claude Code workspace

SynapseMD commands live in the `commands/` folder. Claude Code reads them through `.claude/` symlinks:

```bash
./scripts/link-claude-workspace.sh
```

Verify:

```bash
ls -la .claude/commands
# Should show: .claude/commands -> ../commands
```

You only need to run this once per clone (or again if symlinks break).

---

## Step 4 — Open the project in Claude Code or Cursor

### Option A — Claude Code (recommended)

1. Install Claude Code from [claude.ai/code](https://claude.ai/code)
2. Open a terminal in the `SynapseMD` folder
3. Run:

   ```bash
   claude
   ```

4. Claude Code loads all slash commands from this project automatically

### Option B — Cursor

1. Install [Cursor](https://cursor.com/)
2. Open the `SynapseMD` folder as your workspace
3. Use the integrated Claude agent with slash commands enabled
4. Commands are available because `.claude/commands` symlinks to `commands/`

In both tools, type `/` to see available commands (60+).

---

## Step 5 — Set up your profile (required first step)

Before saving reports or running analysis, set your basic health parameters:

```bash
/profile set 175 70 1990-01-01
```

Replace with your values:

- **175** — height in cm
- **70** — weight in kg
- **1990-01-01** — birth date (YYYY-MM-DD)

Check it saved:

```bash
/profile view
```

SynapseMD uses this to calculate BMI, body surface area (for radiation dose), and age for risk predictions.

---

## Step 6 — Save your first medical report

If you have a lab report or imaging result as an image or PDF:

```bash
/save-report /full/path/to/your-report.jpg
```

Examples:

```bash
/save-report ~/Downloads/blood-test-2025-03-15.jpg
/save-report ./Report/chest-xray.png
```

The system will:

1. Read the image
2. Extract test names, values, and reference ranges
3. Save structured JSON under `data/lab-results/` or `data/imaging/`
4. Back up the original image

Then verify:

```bash
/query all
/query recent 3
```

---

## Step 7 — Record essential health information

Build your record over your first session. You do not need everything on day one — add what you have.

### Allergies

```bash
/allergy add penicillin severe had breathing difficulty as a child
/allergy list
```

### Current medications

```bash
/medication add metformin 500mg twice daily for diabetes
/medication list
```

### Drug interaction check

```bash
/interaction check
```

### Surgery history

```bash
/surgery appendectomy in 2010, no complications
```

### Medical radiation (CT, X-ray)

```bash
/radiation add CT chest 2025-01-10
/radiation status
```

Each command writes to JSON files in `data/`. You can always ask Claude in natural language — it will follow the command definitions.

---

## Step 8 — Run AI analysis on your data

Once you have profile data and some records, try Module 21 AI:

```bash
/ai status
/ai analyze last_quarter
/ai predict hypertension
/ai chat What are my main health trends?
/ai report generate comprehensive last_quarter
```

| Command | What it does |
|---------|--------------|
| `/ai status` | Shows whether AI is configured and what data is available |
| `/ai analyze` | Multi-dimensional analysis across your health trackers |
| `/ai predict` | Risk scores for hypertension, diabetes, cardiovascular, nutrition, sleep |
| `/ai chat` | Ask questions about your stored health data |
| `/ai report` | Generate a structured health report |

AI output is **informational only** — not medical advice or diagnosis. See [Safety](#safety-and-limitations) below.

---

## Step 9 — Get a multi-specialty consultation report

When you have lab or imaging data saved:

```bash
/consult recent 5
```

Or analyze everything:

```bash
/consult all
```

For one specialty only:

```bash
/specialist list
/specialist cardio recent 3
```

These produce structured reports drawing on cardiology, endocrinology, nephrology, and other specialty lenses. Use them to **prepare questions for your doctor**, not as a replacement for medical care.

---

## Your first week — suggested workflow

| Day | Action |
|-----|--------|
| **Day 1** | Clone repo, run setup scripts, set `/profile`, add allergies and medications |
| **Day 2** | `/save-report` for recent lab work; `/query abnormal` |
| **Day 3** | `/interaction check`; record any surgeries or implants with `/surgery` |
| **Day 4** | Start a tracker you care about: `/sleep`, `/nutrition`, `/fitness`, or `/mood` |
| **Day 5** | `/ai analyze last_quarter` and review the output |
| **Day 6** | `/consult recent 5` before an upcoming doctor visit |
| **Day 7** | Back up your `data/` folder (see below) |

Explore more commands anytime with `/` or see the [User Guide](user-guide.md).

---

## Where your data lives

```
SynapseMD/
└── data/                    ← YOUR personal health records (private)
    ├── profile.json         ← height, weight, birth date, BMI
    ├── allergies.json
    ├── medications/
    ├── lab-results/
    ├── imaging/
    ├── ai-config.json
    └── … (60+ tracker files)
```

- **`data/` is not uploaded anywhere** by SynapseMD itself
- Data stays on your filesystem as JSON files
- The `data/` folder is gitignored — it will not be pushed to GitHub if you fork the repo
- **Back up regularly:**

  ```bash
  cp -r data/ ~/Backups/SynapseMD-data-$(date +%Y-%m-%d)
  ```

  Or use Time Machine, cloud backup of a folder you choose, or an encrypted external drive.

---

## Daily commands you'll use most

| Goal | Command |
|------|---------|
| See everything | `/query all` |
| Recent tests | `/query recent 5` |
| Abnormal results | `/query abnormal` |
| Check medications | `/medication list` |
| Check drug interactions | `/interaction check` |
| Log today's meal | `/nutrition add …` |
| Log sleep | `/sleep add …` |
| Ask about your data | `/ai chat …` |
| View profile | `/profile view` |

Full command reference: [User Guide](user-guide.md) · Browse all commands in the [commands/](../commands/) folder.

---

## Optional — Chat UI (AnythingLLM or Open WebUI)

Prefer a **web chat** instead of slash commands in Claude Code? SynapseMD connects to two self-hosted chat UIs. Both talk to the same platform backend — your health data stays on SynapseMD, not in the chat app.

```text
Local CLI path:     Claude Code / Cursor  →  commands/  →  data/ (JSON files)

Chat UI path:       AnythingLLM or Open WebUI  →  platform  →  FHIR + AI tools
```

| UI | Best for | Integration |
|----|----------|-------------|
| **AnythingLLM** | Native MCP support, simpler tool wiring | Direct MCP server (`synapsemd-mcp`) |
| **Open WebUI** | Popular chat UI, rich plugins | OpenAPI bridge (`deploy/openapi-bridge/`) |

**Full Open WebUI guide:** [open-webui-setup.md](open-webui-setup.md)

### Prerequisites (both UIs)

1. **Docker** installed
2. SynapseMD repo cloned
3. ~4 GB free RAM for the full stack

### Shared setup — start platform and get a login token

These steps are the same for AnythingLLM and Open WebUI:

```bash
cd SynapseMD/platform
docker compose --profile full up --build
```

| Service | URL |
|---------|-----|
| SynapseMD API | http://localhost:8000/docs |
| OpenAPI bridge (Open WebUI) | http://localhost:8100 |
| AnythingLLM | http://localhost:3001 |
| Open WebUI | http://localhost:3000 |

**Create your SynapseMD account** (once):

```bash
# Create tenant
TENANT=$(curl -s -X POST http://localhost:8000/api/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"My Health","plan":"starter"}')
TENANT_ID=$(echo "$TENANT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Register user
curl -s -X POST "http://localhost:8000/api/v1/auth/tenants/$TENANT_ID/users" \
  -H "Content-Type: application/json" \
  -d '{"email":"me@example.com","password":"securepass1","role":"patient"}'

# Login — save the token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"me@example.com\",\"password\":\"securepass1\",\"tenant_id\":\"$TENANT_ID\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo "$TOKEN"
```

Verify tools work:

```bash
curl -s -X POST http://localhost:8100/tools/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool":"ai_status","arguments":{}}'
```

### Configure AnythingLLM

AnythingLLM connects **directly** to SynapseMD’s MCP server (recommended integration).

1. Open **http://localhost:3001** and complete the AnythingLLM setup wizard
2. Create or open a **Workspace**
3. Go to **Workspace Settings** → **Agent Skills** → **MCP Servers** (or **Tools** → **MCP**, depending on version)
4. Add a new MCP server:

   | Field | Value |
   |-------|-------|
   | **Name** | `SynapseMD` |
   | **Type** | `stdio` |
   | **Command** | Path to MCP binary (see below) |
   | **Environment** | `SYNAPSEMD_ACCESS_TOKEN=<your token from above>` |

5. **Command options** (pick one):

   **Option A — MCP on your host** (AnythingLLM desktop app or host-installed):

   ```bash
   cd SynapseMD/platform
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[mcp]"
   export SYNAPSEMD_ACCESS_TOKEN="$TOKEN"
   which synapsemd-mcp   # use this full path in AnythingLLM
   ```

   In AnythingLLM MCP config:
   - Command: `/path/to/.venv/bin/synapsemd-mcp`
   - Env: `SYNAPSEMD_ACCESS_TOKEN=<token>`

   **Option B — Docker Compose** (AnythingLLM in browser, MCP via bridge fallback):

   If stdio MCP across containers is awkward, use the **OpenAPI bridge** from Open WebUI instead — call `http://localhost:8100/tools/invoke` from AnythingLLM custom tools, same as Open WebUI.

6. Enable the MCP server for your workspace agent
7. Start a chat and ask, for example:
   - *“Use SynapseMD to check my AI status”*
   - *“Predict my hypertension risk using SynapseMD”*
   - *“Ask SynapseMD: how is my sleep data?”*

**Available MCP tools:** `ai_chat`, `ai_analyze`, `ai_predict`, `ai_report`, `ai_status`, `get_profile_summary`, `query_fhir_records`, `execute_command`, and more. See [ui-mcp-integration.md](ui-mcp-integration.md).

### Configure Open WebUI

Open WebUI uses the **OpenAPI bridge** (not MCP directly).

1. Open **http://localhost:3000** and create your Open WebUI account
2. Add SynapseMD **Functions** (Python tool plugins) that call the bridge
3. Paste your `$TOKEN` and set bridge URL to `http://openapi-bridge:8100`

**Step-by-step with copy-paste function examples:** [open-webui-setup.md](open-webui-setup.md)

Quick test from terminal (same as Open WebUI functions use internally):

```bash
curl -s -X POST http://localhost:8100/tools/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool":"ai_chat","arguments":{"query":"Summarize my available health data"}}'
```

### Chat UI safety reminders

- **Do not paste** lab reports, diagnoses, or IDs into the chat system prompt — use SynapseMD tools instead
- All AI output is **informational only**, not medical advice ([safety-guidelines.md](safety-guidelines.md))
- Chat UIs may store **conversation text** locally; health records stay on the **platform**
- Keep your `$TOKEN` private; re-login if it leaks

### CLI vs chat UI — which to use?

| Use CLI (Claude Code) if… | Use chat UI if… |
|---------------------------|-----------------|
| You want local JSON files only | You prefer a browser chat |
| You use slash commands daily | Your org hosts the platform for you |
| No Docker / platform needed | You want AnythingLLM or Open WebUI |

You can use **both**: CLI for local authoring and data entry; chat UI for conversational access to the platform.

See also: [platform/README.md](../platform/README.md) · [ui-mcp-integration.md](ui-mcp-integration.md)

---

## Troubleshooting

### Slash commands do not appear

```bash
./scripts/link-claude-workspace.sh
ls -la .claude/commands    # must be a symlink to ../commands
```

Restart Claude Code or Cursor after fixing symlinks.

### `data/profile.json` not found

```bash
./scripts/setup-data.sh
```

### `/save-report` cannot read my image

- Use a clear photo or scan (JPG, PNG)
- Provide the full absolute path: `/save-report /Users/you/Downloads/report.jpg`
- Ensure the file exists: `ls /Users/you/Downloads/report.jpg`

### AI commands say not configured

Check that `data/ai-config.json` exists:

```bash
ls data/ai-config.json
./scripts/setup-data.sh    # creates it if missing
```

### I accidentally edited files in `.claude/commands/`

That is fine if symlinks are set up — `.claude/commands` points to the same files as `commands/`. Prefer editing from the repo root for clarity.

### I want to start over without losing the repo

```bash
mv data/ data-backup-$(date +%Y%m%d)
./scripts/setup-data.sh
```

---

## Safety and limitations

SynapseMD follows strict medical safety boundaries:

1. **Does not provide specific medication dosages**
2. **Does not prescribe prescription drugs**
3. **Does not predict life prognosis**
4. **Does not replace a physician's diagnosis**

All analysis, AI output, and consultation reports are **for personal reference and doctor visit preparation only**.

- In an emergency, call your local emergency number immediately
- For mental health crisis, contact a qualified professional or crisis line in your country
- Read the full policy: [safety-guidelines.md](safety-guidelines.md)

---

## What to read next

| Document | When to use it |
|----------|----------------|
| [User Guide](user-guide.md) | Detailed command reference and examples |
| [Open WebUI Setup](open-webui-setup.md) | Step-by-step Open WebUI + SynapseMD configuration |
| [UI & MCP Integration](ui-mcp-integration.md) | AnythingLLM MCP and architecture details |
| [Drug Interaction Database](drug-interaction-database.md) | How interaction severity levels work |
| [Safety Guidelines](safety-guidelines.md) | Medical boundaries and disclaimers |
| [commands/ai.md](../commands/ai.md) | Full AI command options |
| [Developer Guide](developer-guide.md) | Only if you want to extend SynapseMD |

---

## Quick reference — setup checklist

- [ ] Clone: `git clone https://github.com/maruthis/SynapseMD.git`
- [ ] Initialize data: `./scripts/setup-data.sh`
- [ ] Link workspace: `./scripts/link-claude-workspace.sh`
- [ ] Open in Claude Code or Cursor
- [ ] Set profile: `/profile set <height_cm> <weight_kg> <birth_date>`
- [ ] Save first report: `/save-report /path/to/image.jpg`
- [ ] Add allergies and medications
- [ ] Run `/query all` to confirm data saved
- [ ] Try `/ai analyze last_quarter`
- [ ] Back up `data/` folder

You are ready to use SynapseMD.
