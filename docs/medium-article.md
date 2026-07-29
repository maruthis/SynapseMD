# Your Health Data Deserves Better Than Another Cloud App — Introducing SynapseMD

*A personal health vault that grows into an enterprise, PHI-safe AI platform — without forcing you to choose between privacy and intelligence.*

---

## The quiet crisis in personal health data

Most of us treat medical information like email attachments: a PDF here, a portal login there, a photo of a lab report buried in camera roll. When a clinician asks, “What were your numbers last year?” we shrug and scroll.

Consumer health apps promised to fix this. Many of them did the opposite. They asked for cloud uploads, buried the real ownership story in a privacy policy, and optimized for engagement — not for a durable, portable record you control.

Meanwhile, enterprises are racing to bolt chatbots onto clinical workflows. The risk is obvious: large language models are powerful, and unprotected health information (PHI) does not belong in an undifferentiated prompt log.

**SynapseMD** started as an answer to a simpler question:

> Can I manage my health data the way developers manage code — locally, versionable, scriptable — and still get serious AI help?

The answer turned into something larger: a system that works for a single person with JSON files on disk, *and* for a multi-tenant platform with FHIR, MCP tools, and audit trails.

**GitHub:** [https://github.com/maruthis/SynapseMD](https://github.com/maruthis/SynapseMD)

---

## What SynapseMD is (in one paragraph)

SynapseMD is an open-source **personal health information system** with an optional **enterprise platform**. Locally, you use slash commands in Cursor or Claude Code against a file-based health vault. In production mode, the same intelligence engine runs behind FastAPI, JWT auth, FHIR-backed storage, PHI anonymization, and an MCP server that chat UIs like AnythingLLM and Open WebUI can call.

It is **not** a replacement for a physician. It is a structured memory and analysis layer — with guardrails — so you (or your organization) can ask better questions of your own data.

---

## Two modes, one intelligence layer

| Mode | Best for | How you use it |
|------|----------|----------------|
| **CLI / personal** | Individuals, clinicians who live in the terminal | `/profile`, `/save-report`, `/consult`, `/ai` over `data/` JSON |
| **Platform** | Multi-tenant products, assistants, pilots | REST `/api/v1/*`, MCP tools, Docker Compose / Kubernetes |

Both modes share **Module 21** — the AI prediction and analysis engine — so risk models and safety posture stay aligned whether you are typing `/ai predict hypertension` or calling `ai_predict` over MCP.

That dual path matters strategically. You can prototype on your laptop without standing up Postgres. When you are ready for tenants, chat UIs, and compliance-minded deployment, you graduate the same product — not a rewrite.

---

## How it feels day to day

### 1. Set a profile

```bash
/profile set 175 70 1990-01-01
```

Height, weight, birth date — stored as structured JSON under `data/`.

### 2. Ingest a lab report

```bash
/save-report ~/Downloads/blood-panel.pdf
```

The system extracts values, flags abnormals, and indexes the record for later query and AI analysis.

### 3. Ask the vault

```bash
/query recent 5
/allergy list
/prepare Cardiology
```

Visit prep can pull allergies, meds, recent labs, and department-specific checklists — the kind of briefing you wish every portal produced.

### 4. Run AI with eyes open

```bash
/ai status
/ai predict hypertension
/ai analyze last_quarter
```

### 5. Multidisciplinary consult

```bash
/consult recent 5
```

Specialist lenses (cardiology, endocrinology, neurology, and more) reason over the same record set and a coordinator synthesizes priorities. It is opinionated software, not a diagnosis machine.

---

## Using LLMs appropriately in regulated environments

“Add ChatGPT to healthcare” is easy to demo and hard to defend. SynapseMD treats LLM use as a **controlled capability**, not the system of record.

When the platform path calls an external model, the design goals are deliberately compliance-minded:

1. **Minimize what the model sees** — PHI anonymization / tokenization before LLM calls; chat UIs stay thin and must not become the vault for labs and FHIR bundles.  
2. **Know who called what** — JWT auth, tenant isolation (including Postgres RLS), scoped MCP tokens (`SYNAPSEMD_ACCESS_TOKEN`).  
3. **Audit without replaying secrets** — audit events emphasize hashes and metadata, not raw prompt dumps of patient identifiers.  
4. **Route by risk** — `HealthLLMRouter` picks model tier by command complexity and data sensitivity; critical workflows can require human review.  
5. **Gate production providers** — `LLM_DEFAULT_PROVIDER` (`mock` / `anthropic` / `openai` / `google`) plus BAA flags (`*_BAA_SIGNED`) so staging/production cannot casually enable a vendor without a signed Business Associate Agreement posture.  
6. **Prefer determinism where it is safer** — Module 21 risk scoring (`ai/prediction.py`) is largely evidence-based local logic (`synapsemd-ai`), not an unconstrained free-form diagnosis from a general LLM.  
7. **Say what the system will not do** — no autonomous prescribing, no “replacing the physician,” mandatory disclaimers.

The product claim for regulated buyers is not “we use AI.” It is: **we can place AI next to sensitive data only after isolation, anonymization, routing, and audit are in place** — and we can keep `mock` providers in lower environments until BAAs and ops reviews are ready.

---

## Enterprise-grade software as markdown: commands, skills, specialists

Most enterprise AI products bury behavior in opaque services. SynapseMD’s product surface is **versionable artifacts** — closer to how you extend a developer toolchain than how you ship a closed mobile app.

| Layer | Folder | What it is |
|-------|--------|------------|
| **Commands** | `commands/*.md` | User-facing slash commands (`/sleep`, `/allergy`, `/consult`, …) — ~59 today |
| **Skills** | `skills/*/SKILL.md` | Deep analyzers and report recipes (sleep, nutrition, trends, travel health, …) |
| **Specialists** | `specialists/*.md` | Clinical lenses for MDT consults (cardiology, endocrinology, oncology, …) |

That separation is the extensibility model:

- **Command** = the verb the user types and the CRUD / workflow contract  
- **Skill** = how to analyze a domain in depth (often reusable across commands)  
- **Specialist** = a professional perspective applied during `/consult` / `/specialist`

### Extend without a big rewrite

In practice, adding capability often means **adding markdown**, not inventing a new microservice.

**Example — add a specialist lens** (pattern already used for cardiology, nephrology, psychiatry, …):

1. Create `specialists/rheumatology.md` with role, red flags, what data to read, and how to phrase recommendations.  
2. Wire it into the consultation coordinator’s specialty list (documented in the [developer guide](https://github.com/maruthis/SynapseMD/blob/main/docs/developer-guide.md)).  
3. Run `/consult` — the new lens participates without rewriting the FastAPI stack.

**Example — add a skill** (pattern used by `sleep-analyzer`, `nutrition-analyzer`, `health-trend-analyzer`, …):

1. Create `skills/my-domain-analyzer/SKILL.md` with analysis steps, inputs from `data/`, and output structure.  
2. Optionally add a thin command in `commands/` that invokes that skill.  
3. Seed `data-example/` so demos and tests have schemas.

**Example — add a command** (pattern used across allergies, vaccines, chronic disease trackers):

1. Add `commands/my-command.md` with frontmatter (`description`, arguments) and action types (`add` / `list` / …).  
2. Define or reuse a JSON tracker under `data-example/`.  
3. Document usage; platform MCP/REST can later expose the same orchestrated behavior when you need multi-tenant access.

Subject-matter experts and technical writers can draft much of this. Engineers still own safety checks, tests, and platform wiring — but **day-to-day domain growth is artifact-driven**. That is how you get enterprise breadth (dozens of workflows) without a linear explosion of custom UI screens.

For enterprises, the same artifacts sit behind:

- Multi-tenant JWT auth and RBAC  
- FHIR migration paths and optional HAPI  
- PHI anonymization before model calls  
- Hash-oriented audit events  
- Medical guardrails and a human-review queue  
- MCP (SSE for Docker) plus an OpenAPI bridge for Open WebUI  
- Docker Compose profiles and Kubernetes overlays  

Quality bar today: **266+ automated tests**, **≥98% coverage** on the gate that ships with the repo.

---

## Privacy is a product requirement, not a slogan

1. **Local-first for personal use** — your vault can live entirely on disk.  
2. **Chat UIs are thin** — AnythingLLM / Open WebUI should not become the system of record for labs and FHIR bundles.  
3. **Tokens are scoped** — platform MCP tools authenticate with a SynapseMD JWT, not a vague “trust the chatbot.”  
4. **Safety language is mandatory** — informational analysis, not prescribing or autonomous diagnosis.

---

## Getting started in ten minutes

```bash
git clone https://github.com/maruthis/SynapseMD.git
cd SynapseMD
./scripts/setup-data.sh
./scripts/link-claude-workspace.sh
```

Open the repo in Cursor or Claude Code, then:

```bash
/profile set 175 70 1990-01-01
/query all
```

Prefer the platform + chat UI path?

```bash
cd platform
docker compose --profile full up --build -d
```

Docs worth bookmarking:

- [Getting started](https://github.com/maruthis/SynapseMD/blob/main/docs/getting-started.md)  
- [Developer guide — extend commands/skills/specialists](https://github.com/maruthis/SynapseMD/blob/main/docs/developer-guide.md)  
- [AnythingLLM + MCP](https://github.com/maruthis/SynapseMD/blob/main/docs/anythingllm-setup.md)  
- [Open WebUI setup](https://github.com/maruthis/SynapseMD/blob/main/docs/open-webui-setup.md)  
- [LLM choice (platform)](https://github.com/maruthis/SynapseMD/blob/main/platform/README.md#llm-choice)  

---

## One codebase, many levels of adoption

SynapseMD is intentionally staged so different personas can stop at the right altitude:

| Persona | How they use it | What they get |
|---------|-----------------|---------------|
| **Developer on a laptop** | Clone repo, `setup-data.sh`, slash commands in Cursor/Claude Code | Private JSON vault, `/ai`, `/consult`, full command catalog — no cloud required |
| **Advanced developer / integrator** | Run `synapsemd-mcp` (stdio or Docker SSE on `:8081`), wire AnythingLLM / Open WebUI / custom agents | Same tools over **MCP**; assistant UIs without rewriting clinical logic |
| **Clinic / personal assistant to a doctor** | Platform + MCP/OpenAPI bridge, tenant JWT, visit prep (`/prepare`), MDT-style `/consult`, review queue | A PHI-aware aide for briefing and synthesis — **not** an autonomous clinician |
| **Enterprise product / ops** | Multi-tenant FastAPI, FHIR, RLS, K8s overlays, BAA-gated LLM providers, audit, release gates | Centralized (tenant-scoped) data plane, governed AI, deployable assistants at scale |
| **Platform of the future** | Learning loop, eval gates, feedback APIs, certified connectors (roadmap) | Continuous improvement **without** storing raw PHI in learning stores; centralized intelligence with decentralized trust boundaries |

You do not have to “go enterprise on day one.” The same repository supports a weekend personal vault *and* a path toward multi-tenant assistants with continuous learning and centralized operational data — when governance catches up to ambition.

---

## Beyond healthcare: the same pattern for other regulated verticals

Health is the first vertical because PHI makes the constraints obvious. The **architecture pattern** — markdown commands, deep skills, role specialists, local vault → multi-tenant platform, MCP distribution, anonymize-before-LLM, audit hashes, human review — generalizes.

Imagine the same skeleton renamed for another domain:

| Vertical | Commands (examples) | Skills | Specialists / roles |
|----------|---------------------|--------|---------------------|
| **Legal** | `/matter`, `/clause`, `/deadline` | Contract risk analyzer, precedent research skill | Litigation, corporate, IP counsel lenses |
| **Compliance** | `/policy`, `/control`, `/evidence` | Control-mapping skill, gap analysis | SOX, GDPR, SOC 2 reviewers |
| **HR** | `/employee`, `/policy-ack`, `/case` | Policy Q&A skill, case-trend analyzer | ER, benefits, recruiting advisors |
| **Finance / risk** | `/exposure`, `/recon` | Anomaly skill, narrative report skill | Credit, ops risk, audit lenses |

In each case, subject-matter experts author **markdown workflows**; engineers keep the platform rails (tenancy, secrets, model routing, audit). You get enterprise-shaped software that stays **extendable without a ticket for every new screen** — because much of the product *is* the markdown.

SynapseMD proves the pattern in healthcare. The invitation to builders in Legal, Compliance, HR, and adjacent regulated domains is: **reuse the rails; rewrite the artifacts.**

---

## What’s next on the healthcare roadmap

The foundation (auth, MCP, AI, anonymization, audit, release gates) is in place. Near-term build priorities include:

1. **FHIR-primary platform** — clinical graph hardening and migration completeness  
2. **Learning loop** — eval gates, feedback signals, clinician review UX (without storing PHI in learning stores)  
3. **Generative health UI** — AG-UI-style charts and human-in-the-loop flows beyond chat text  
4. **Enterprise connectors** — certified tiers toward SMART-on-FHIR and, carefully, EHR integrations  

The bet is straightforward: AI in regulated domains only scales if **governance and data architecture** scale with the demos.

---

## Closing

We optimized editors, CI, and cloud bills for a decade. SynapseMD is an experiment in applying the same craft to something harder: sensitive domain data you can inspect, extend as markdown, and eventually operationalize — with LLMs that are useful *because* they are constrained.

Whether you are a developer with a local vault, an integrator shipping MCP tools, a clinic piloting a doctor’s assistant, or a team building the next vertical on the same pattern — the repository is meant to meet you where you are.

If that resonates, star the repo, try the getting-started guide, and tell us what command — or what vertical — you wish existed next.

**Repo:** [github.com/maruthis/SynapseMD](https://github.com/maruthis/SynapseMD)

---

### Disclaimer

SynapseMD is for personal health information management and decision *support* context only. It does **not** provide medical diagnosis, treatment, or prescribing advice. Always consult a qualified healthcare professional for medical decisions. In emergencies, contact emergency services. Analogous disclaimers apply if the pattern is adapted to Legal, Compliance, HR, or other domains: the system assists professionals; it does not replace licensed judgment.

*Independent open-source project. Not affiliated with Anthropic or Claude.ai.*

---

### Suggested Medium tags

`Health Tech` · `Open Source` · `Artificial Intelligence` · `Privacy` · `FHIR` · `MCP` · `Enterprise Software` · `Compliance` · `Developer Tools`

### Suggested subtitle (Medium)

*PHI-safe LLM use, markdown-extensible commands/skills/specialists, and a path from laptop vault to enterprise assistants — plus why the same pattern fits Legal, Compliance, and HR.*
