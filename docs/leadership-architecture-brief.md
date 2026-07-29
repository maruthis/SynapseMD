# SynapseMD Architecture Brief for Leadership

**Purpose:** Present how SynapseMD is designed so product, clinical, and technology leaders can evaluate **extensibility, scalability, and go-to-market fit** — without diving into implementation minutiae.

**Audience:** Executive / product / architecture leadership  
**Companion technical deep-dive:** [architecture.md](architecture.md) · [individual-user-guide.md](individual-user-guide.md) · [developer-guide.md](developer-guide.md)

**One-line thesis**

> SynapseMD separates a stable **technical platform** from a growing set of **domain capabilities expressed as markdown artifacts** — so clinical and lifestyle features can expand continuously without rewriting the core architecture, while the same intelligence layer serves IDE agents and chatbot UIs.

---

## Table of contents

1. [Executive snapshot](#1-executive-snapshot)
2. [Artifact-driven architecture](#2-artifact-driven-architecture)
3. [Technical features vs domain features](#3-technical-features-vs-domain-features)
4. [Domain capability map](#4-domain-capability-map)
5. [Continuous feature addition without architectural change](#5-continuous-feature-addition-without-architectural-change)
6. [Scalability model](#6-scalability-model)
7. [UI flavors — one intelligence, many surfaces](#7-ui-flavors--one-intelligence-many-surfaces)
8. [Workflow support](#8-workflow-support)
9. [Data ingestion](#9-data-ingestion)
10. [Governance and trust](#10-governance-and-trust)
11. [Leadership takeaways](#11-leadership-takeaways)
12. [Appendix — talking points](#12-appendix--talking-points)

---

## 1. Executive snapshot

| Dimension | What leadership should know |
|-----------|------------------------------|
| **Product shape** | Personal → clinic assistant → multi-tenant platform — **one product family**, staged adoption |
| **Differentiation** | Domain logic lives in **reviewable markdown** (commands, skills, specialists), not only buried in application code |
| **Speed to new capability** | Add a specialty lens or analyzer largely by adding files — **no redesign of auth, tenancy, or MCP** |
| **Channels** | Claude Code / Cursor CLI · Open WebUI · AnythingLLM · custom agents via MCP/REST |
| **Risk posture** | AI is decision **support**; PHI path includes anonymization, audit hashes, guardrails (platform mode) |

```text
                    ┌─────────────────────────────────────┐
                    │     Domain artifacts (markdown)     │
                    │  commands · skills · specialists    │
                    └─────────────────┬───────────────────┘
                                      │ interpreted by
                    ┌─────────────────▼───────────────────┐
                    │     Technical rails (stable)        │
                    │  agent runtime · API · MCP · AI     │
                    │  auth · storage · audit · safety    │
                    └─────────────────┬───────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
         IDE / CLI              Chatbot UIs              Future apps
      (Cursor/Claude)        (Open WebUI / ALLM)         (REST/MCP)
```

---

## 2. Artifact-driven architecture

### What “artifact-driven” means

Most health AI products encode workflows inside closed services and UI screens. SynapseMD encodes **behavior as versionable artifacts**:

| Artifact | Location | Leadership meaning |
|----------|----------|---------------------|
| **Command** | `commands/*.md` | The **product verb** the user (or agent) invokes — UX contract, arguments, data paths |
| **Skill** | `skills/*/SKILL.md` | **How** to analyze a domain in depth (reusable across commands) |
| **Specialist** | `specialists/*.md` | **Clinical perspective** for MDT-style consults |
| **Data schema** | `data-example/` → `data/` | Persistence contracts for each domain |
| **Platform** | `platform/` | Optional enterprise rails (auth, FHIR, MCP, anonymize, audit) |

### Why this matters commercially

1. **SME participation** — Clinicians and domain authors can draft specialty lenses and analyzers as markdown; engineers keep rails and safety.
2. **Auditability** — Behavior is diffable in Git (what changed in cardiology guidance last quarter?).
3. **Portfolio speed** — New vertical or disease area ≈ new artifact pack, not a new microservice per feature.
4. **Same artifacts, multiple channels** — CLI and chat UIs consume the same intelligence model (with runtime differences noted below).

### Simplified runtime (personal / IDE)

```text
User intent (/consult, /save-report, /ai …)
        │
        ▼
  Agent (Cursor / Claude Code)
        │  reads artifacts
        ├── commands/*.md
        ├── skills/*/SKILL.md
        └── specialists/*.md
        │
        ├── read/write → data/ (JSON vault)
        └── output → Report / chat response
```

---

## 3. Technical features vs domain features

SynapseMD draws a **hard line** between what is *infrastructure* and what is *health domain product*.

### Technical features (the rails — change rarely)

Owned primarily as **code** in `platform/`, `scripts/`, and agent tooling:

| Technical capability | Role |
|----------------------|------|
| Authentication & tenancy | JWT, RBAC, tenant isolation / RLS |
| API & MCP distribution | REST `/api/v1/*`, MCP tools for chat UIs |
| PHI protection | Anonymize before LLM; hash-oriented audit |
| Model routing | Complexity / sensitivity → provider tier |
| Guardrails & human review | Clinical safety posture for critical flows |
| Deterministic AI scoring | Module 21 risk engine (`synapsemd-ai`) |
| Storage adapters | Local JSON vault · FHIR-backed platform |
| Deployment | Docker Compose profiles · K8s overlays |

### Domain features (the product surface — change often)

Owned primarily as **markdown (+ JSON schemas)**:

| Domain layer | Examples |
|--------------|----------|
| Commands (~59) | `/profile`, `/save-report`, `/diabetes`, `/consult`, `/ai` |
| Skills (~19 analyzers) | Sleep, nutrition, trends, travel health, AI analyzer, goals |
| Specialists (MDT lenses) | Cardiology, endocrinology, nephrology, gastroenterology, … |

**Rule of thumb for leadership**

> If the question is *“What should a cardiologist emphasize on these labs?”* → **domain markdown**.  
> If the question is *“How do we keep PHI out of the model log?”* → **technical platform**.

That separation is intentional: domain teams expand coverage; platform teams harden trust and scale.

---

## 4. Domain capability map

Domain features group into product portfolios — each largely artifact-backed:

| Portfolio | Illustrative capabilities |
|-----------|---------------------------|
| **Clinical support** | Visit prep (`/prepare`), MDT consult (`/consult`), specialty consult (`/specialist`), meds / interactions / polypharmacy, chronic disease (HTN, diabetes, COPD), lab & imaging vault |
| **Lifestyle & prevention** | Sleep, fitness, nutrition, diet, goals & habits |
| **Life-stage & specialty** | Women’s / men’s / child health, mental health, eye / oral / skin, rehab, fall risk, travel, occupational, TCM |
| **AI insight layer** | `/ai analyze`, `/ai predict`, `/ai chat`, `/ai report` (Module 21 + agent analysis) |
| **Reporting** | Structured JSON vault + HTML / briefing outputs |

**Leadership framing:** Clinical support and lifestyle are **first-class product lines**, not afterthoughts bolted onto a chatbot. They share the same artifact model and data vault.

---

## 5. Continuous feature addition without architectural change

### The extension pattern

| New business need | Typical change | Touch technical rails? |
|-------------------|----------------|------------------------|
| New specialty (e.g. rheumatology) | Add `specialists/rheumatology.md`; wire into consult routing list | Usually **no** |
| New deep analyzer | Add `skills/my-analyzer/SKILL.md` | Usually **no** |
| New user workflow | Add `commands/my-command.md` + `data-example` schema | Usually **no** |
| New chat UI | Configure MCP URL / OpenAPI bridge | **Config only** |
| New LLM vendor | Provider + BAA flags in platform config | Config / thin adapter |
| New enterprise control | Auth, audit, RLS, FHIR | Platform change (by design) |

### Organizational implication

- **Domain velocity** is decoupled from **platform release cadence**.
- Platform ships trust, tenancy, and distribution; domain ships clinical breadth.
- Avoids the classic failure mode: “every new disease needs a new microservice and a new screen.”

```text
Time →
Domain pack v1 (core) ──► + sleep/nutrition ──► + MDT specialties ──► + new vertical pack
Technical rails v1 ──────────────────────────── stable ──────────────────► selective upgrades
```

---

## 6. Scalability model

Scalability is **staged**, not all-or-nothing:

| Scale stage | Architecture posture | Who it serves |
|-------------|----------------------|---------------|
| **1. Personal / laptop** | JSON vault + IDE agent | Individual, developer, single clinician |
| **2. Clinic assistant** | Same artifacts + local platform + MCP chat UI | Doctor personal assistant, small practice |
| **3. Multi-tenant product** | FastAPI, JWT, FHIR, RLS, anonymization, audit | B2B / org pilots |
| **4. Enterprise ops** | Compose → Kubernetes, SLOs, release gates, connectors roadmap | Regulated deployments |

### What scales without rewriting domain packs

- **Horizontal reach** — More tenants / users on the platform rails  
- **Channel reach** — More UIs via MCP/REST without rewriting `/consult` markdown  
- **Domain breadth** — More commands/skills/specialists as markdown packs  
- **Model spend control** — Route by command risk (`HealthLLMRouter`)  
- **Learning loop (roadmap)** — Eval / feedback without storing raw PHI in learning stores  

### What “scalable” means here

Not only “more CPU.” It means:

1. **Capability scale** — dozens of workflows without UI explosion  
2. **Org scale** — multi-tenant isolation when needed  
3. **Channel scale** — CLI and chatbots on one intelligence layer  
4. **Governance scale** — anonymize, audit, guardrails grow with AI usage  

---

## 7. UI flavors — one intelligence, many surfaces

| UI flavor | How users interact | Best fit |
|-----------|--------------------|----------|
| **Claude Code / Cursor (CLI slash commands)** | `/profile`, `/consult`, `/ai` … agent executes markdown playbooks | Highest fidelity workflows; developers; MDT fan-out |
| **AnythingLLM** | Chat → MCP SSE tools | Familiar assistant UX |
| **Open WebUI** | Chat → Workspace Tools / MCP / OpenAPI bridge | Browser-based clinical aide |
| **Custom / future apps** | REST `/api/v1/*` + MCP | Product embedding |

```text
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Cursor/Claude│  │ AnythingLLM  │  │  Open WebUI  │
│  slash cmds  │  │  chat + MCP  │  │ tools + MCP  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       │            MCP / REST             │
       │                 │                 │
       └────────────┬────┴────┬────────────┘
                    ▼         ▼
              Domain artifacts + Module 21 AI
              (+ platform rails when multi-tenant / chat)
```

**Leadership point:** We do not rebuild clinical logic per UI. We **distribute** the same capability surface. Chat UIs remain thin; the vault / platform remains the system of record.

---

## 8. Workflow support

SynapseMD is workflow-native: commands are **multi-step playbooks**, not single API clicks.

| Workflow class | Example | How it is supported |
|----------------|---------|---------------------|
| **Onboarding** | Set profile → seed vault | `/profile`, setup scripts |
| **Ingest → structure → index** | Lab PDF → JSON → `index.json` | `/save-report` |
| **Query & prep** | Recent labs → visit briefing | `/query`, `/prepare` |
| **Chronic management** | Glucose / BP tracking over time | `/diabetes`, `/hypertension`, … |
| **Safety check** | Drug interaction / polypharmacy | `/interaction`, `/polypharmacy` |
| **MDT synthesis** | Abnormal labs → multi-specialty opinions → coordinator merge | `/consult` + specialists |
| **Risk & insight** | Predict diabetes; quarterly analysis | `/ai predict`, `/ai analyze` |
| **Reporting** | HTML / briefing for clinician or patient | `/report`, `/ai report` |
| **Goals & habits** | SMART goals, streaks | `/goal` + goal-analyzer skill |

### MDT workflow (illustrative)

```text
/consult recent 5
   → collect scoped exams
   → route abnormals to specialties
   → parallel specialist artifacts
   → consultation-coordinator merges priorities
   → disclaimers + recommended next clinical steps
```

Workflows are **composable**: ingest once, then prep / consult / AI / report without re-entering data.

---

## 9. Data ingestion

SynapseMD supports multiple ingestion styles into one vault / platform model:

| Ingestion path | Mechanism | Output |
|----------------|-----------|--------|
| **Lab / imaging reports** | `/save-report` (PDF/image → structured extract) | `biochemical-tests/` or `imaging-examinations/` + `index.json` |
| **Manual structured entry** | Domain commands (`/allergy add`, `/medication add`, `/symptom`, …) | Domain JSON trackers |
| **Lifestyle & wearables-style logging** | `/sleep`, `/fitness`, `/nutrition`, `/diet`, `/goal` | Tracker JSON |
| **Assessment instruments** | Mental health, cognitive, screening commands | Scored records |
| **Family / history narratives** | `/family`, `/surgery`, `/discharge` | Structured history |
| **Platform / API (chat or apps)** | REST / MCP tools with auth | Tenant-scoped store (FHIR path on platform) |
| **Templates & migration** | `setup-data.sh`, example schemas, FHIR migration tooling | Consistent schemas |

**Design principles for ingestion**

1. **Normalize early** — Prefer structured JSON over keeping only PDFs in chat history.  
2. **Index for recall** — Global `index.json` (local) enables `/query` and consult scoping.  
3. **Preserve provenance** — Original files stored alongside extracted items when using `/save-report`.  
4. **Identity discipline** — Leadership should treat mismatched patient labels on source reports as an operational risk (vault hygiene).  

---

## 10. Governance and trust

Brief points for leadership risk conversations:

| Control | Intent |
|---------|--------|
| Local-first personal mode | PHI can remain on-disk |
| Thin chat UIs | Assistants do not become the EHR |
| Anonymize-before-LLM (platform) | Reduce PHI in model prompts |
| Audit hashes | Accountability without replaying secrets |
| Guardrails + disclaimers | Decision support, not autonomous care |
| BAA-gated providers | Production model enablement with vendor posture |
| Deterministic Module 21 scoring | Risk math not solely free-form LLM |

---

## 11. Leadership takeaways

1. **Artifact-driven** — Product behavior is largely commands, skills, and specialists in markdown.  
2. **Clear separation** — Technical rails (auth, MCP, PHI, routing) vs domain packs (clinical, lifestyle, life-stage).  
3. **Breadth without rewrite** — Clinical support, lifestyle, and specialty areas expand as artifact packs.  
4. **Continuous delivery of features** — New specialty/analyzer/workflow often needs **no** architectural change.  
5. **Scalable by stage** — Laptop → clinic assistant → multi-tenant → enterprise ops on the same family.  
6. **UI-agnostic intelligence** — Claude CLI and chatbot UIs (AnythingLLM, Open WebUI) share the capability layer.  
7. **Workflow-native** — Ingest, prep, consult, AI, and report compose into end-to-end journeys.  
8. **Ingestion diversity** — Reports, manual entry, lifestyle logs, assessments, and API/MCP all feed one structured store.

**Investment ask framing (optional narrative):** Fund **platform trust & distribution** once; fund **domain packs** repeatedly as the growth engine.

---

## 12. Appendix — talking points

### 60-second pitch

“SynapseMD is a health intelligence system where clinical and lifestyle capabilities are markdown artifacts running on stable technical rails. We can add cardiology or sleep analysis without rebuilding auth or chat connectors. The same engine serves a developer in Cursor or a doctor in Open WebUI / AnythingLLM, and scales from a private vault to multi-tenant deployment when governance is ready.”

### Likely questions

| Question | Short answer |
|----------|--------------|
| Is this just another chatbot? | No — structured vault + workflows + specialty artifacts; chat is one channel. |
| Who writes new features? | Domain experts draft markdown; engineers own rails and safety. |
| How fast can we add a specialty? | Often days for a specialist pack, not a platform rewrite. |
| Does every UI get full MDT? | IDE path has richest specialist fan-out today; platform exposes governed tools (AI/commands) over MCP/REST. |
| How do we stay compliant? | Local-first option; platform adds anonymization, audit, tenancy, guardrails, BAA gates. |

### Related materials

| Doc | Use |
|-----|-----|
| [architecture.md](architecture.md) | Technical architecture + command flow diagrams |
| [individual-user-guide.md](individual-user-guide.md) | Developer & doctor personal-assistant usage |
| [commands-catalog.md](commands-catalog.md) | Full command list |
| [medium-article.md](medium-article.md) | Narrative for broader audiences |
| [platform/README.md](../platform/README.md) | API / MCP / deployment |

---

*SynapseMD leadership architecture brief — for internal presentation use. Not a clinical protocol. Outputs of the system are decision support only.*
