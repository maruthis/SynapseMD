# SynapseMD SOP → Case Procedure Architecture and Design

**Document ID:** SYN-ARCH-SOP-CASE-001  
**Status:** Draft Architecture & Design Proposal  
**Date:** 2026-08-20  
**Audience:** Engineering, Architecture, Security, Compliance, Product, Clinical / Operational SMEs  
**Companions:**
- SynapseMD Enterprise Platform — Architecture and Design (SYN-ARCH-ENT-001)
- SynapseMD Dynamic Case Management (SYN-ARCH-DCM-001)
- ROM-SOP-007 (SOP on SOP) · HKP-SOP-001 (Terminal Cleaning of Isolation Room)

**Primary AI agent framework:** [Pydantic AI](https://github.com/pydantic/pydantic-ai) ([docs](https://ai.pydantic.dev/), [pydantic.dev](https://pydantic.dev/))

---

## 1. Executive Summary

SynapseMD extends the enterprise platform with a **SOP-driven, procedure-bound case capability**. Organizations run on controlled SOPs. The platform does not “interpret PDFs at runtime.” It **compiles** SOPs into versioned artifacts, then **executes** them under deterministic gates while humans perform work and agents advise.

### One-liner pipeline (locked)

```text
SOP
  → compiled Case Playbook + Policies + Task templates
  → Case Runtime (deterministic gates)
  → MCP adapters
  → humans execute, agents advise, platform enforces
```

### Three primary layers

| Layer | Owns | Does not own |
|-------|------|----------------|
| **Platform Layer** | Trust, identity, authZ, audit, PHI, LLM routing, MCP server, persistence, observability | Domain SOP content |
| **Artifact Layer** | Versioned playbooks, policies, task templates, commands, skills, specialists | Runtime case state mutation |
| **Procedure Layer (CASE plane)** | Case aggregate, PROCEDURE_BOUND execution, gates, events, twin updates; **SOP compile / promote helpers** | Bypassing Platform trust controls |

**Pydantic AI** is the framework for **typed, dynamic agent creation** (advice agents, SOP-compile agents, specialist review agents). It is **not** the workflow engine and **not** the authority for room release, SoD, or mandatory steps.

---

## 2. Design Principles

1. **Domain stays artifact-driven; platform owns trust.** Same philosophy as SynapseMD enterprise and DCM docs.
2. **Deterministic-first.** Safety rules, SoD, SLA timers, release gates, competency checks, and case closure are code + policy JSON — never LLM free-text.
3. **AI proposes; policy constrains; humans decide.** Aligns with HKP-SOP-001 FAQ 23.4 and Section 8 (AI must not authorize release alone).
4. **Compile, then pin.** Cases pin playbook/policy/template versions at create time. No silent hot-reload mid-flight.
5. **PROCEDURE_BOUND ≠ adaptive DCM.** Same case tables; different orchestration mode. Adaptive goal-driven plans are a later mode.
6. **MCP is the integration and capability boundary**, not the process definition language.
7. **Pydantic AI agents are typed and allowlisted.** Tools are fixed schemas; model output is Pydantic-validated; agents cannot invent privileged tools.
8. **Procedure Layer may generate Artifact Layer drafts** from SOPs; only human-approved promotion makes artifacts `ACTIVE`.
9. **Reuse existing trust plane.** No parallel auth, audit, consent, or PHI path.
10. **Thin commands; fat tasks.** SOP procedure rows become task instances, not dozens of command-catalog entries.

---

## 3. Layered Architecture Overview

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ EXPERIENCE                                                               │
│  Mobile / PWA · CLI · AnythingLLM / Open WebUI · Partner apps            │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │ REST + MCP (JWT)
┌────────────────────────────────▼─────────────────────────────────────────┐
│ 1. PLATFORM LAYER                                                        │
│  Identity · RBAC/ABAC · Consent · Audit · Guardrails · LLM Policy        │
│  Anonymization · Object Store · OTel · Postgres SoR + RLS                │
│  FastAPI · CommandOrchestrator · synapsemd-mcp                           │
│  Pydantic AI runtime host (model routing, deps, tracing)                 │
└────────────┬───────────────────────────────┬─────────────────────────────┘
             │                               │
┌────────────▼─────────────┐   ┌─────────────▼─────────────────────────────┐
│ 2. ARTIFACT LAYER        │   │ 3. PROCEDURE LAYER (CASE plane)           │
│  Artifact Registry       │◄──│  CaseService · GateEngine · TaskEngine    │
│  Playbooks · Policies    │   │  Event journal · Outbox · Twin adapters   │
│  Task templates          │   │  Advice agents (Pydantic AI)              │
│  Commands · Skills       │   │  SOP Compiler agents (Pydantic AI) ────────┼──► drafts → Artifact Layer
│  Specialists · Profiles  │   │  PROCEDURE_BOUND interpreter              │
└──────────────────────────┘   └───────────────────────────────────────────┘
```

**Data flow (happy path):**

```text
SOP (DMS / PDF / structured import)
        │
        ▼
Procedure Layer — SOP Compiler (Pydantic AI + schema validators)
        │  produces DRAFT artifacts
        ▼
Human review gate (Quality / IPC / Function Head per ROM-SOP-007)
        │
        ▼
Artifact Layer — ACTIVE playbook + policies + task templates
        │
        ▼
Event (e.g. room.vacated) → Case Runtime instantiates PROCEDURE_BOUND case
        │
        ▼
Humans complete tasks via API/MCP · Agents advise via Pydantic AI
        │
        ▼
GateEngine enforces · Twin/Bed Mgmt updated · Audit + KPIs
```

---

## 4. The Platform Layer

### 4.1 Role

The Platform Layer is the **enterprise trust and execution substrate** already largely delivered in Phases A–E of `synapsemd_platform`. The CASE and Artifact planes plug into it; they do not fork it.

### 4.2 Responsibilities

| Concern | Current / extended components |
|---------|--------------------------------|
| Identity & sessions | OIDC, JWT, sessions, break-glass |
| Authorization | `auth/roles.py`, `auth/policy.py` + new case scopes/roles |
| Consent & purpose | `auth/consent.py`, LLM processing gates |
| PHI | Anonymization engine, Vault tokens |
| Persistence | PostgreSQL + Alembic + RLS |
| Audit | Append-only hash-chained `audit` events |
| Command entry | `CommandOrchestrator`, `POST /commands/execute` |
| MCP server | `synapsemd_platform.mcp` (stdio / SSE) |
| LLM routing | `ModelPolicyEngine`, `HealthLLMRouter`, BAA/residency |
| Medical guardrails | `governance/guardrails.py` (advice text) |
| Human AI review | `review_queue` + `/review/*` (for AI recommendations) |
| Object storage | Evidence blobs (photos, downtime forms) |
| Observability | OpenTelemetry; optional [Pydantic Logfire](https://pydantic.dev/) for agent traces |
| Agent host | **Pydantic AI** `Agent` lifecycle, deps injection, model string via existing policy |

### 4.3 What Platform explicitly does not do

- Author SOP content
- Invent procedure steps at runtime
- Autonomously release isolation rooms or close Tier-1 gates
- Expose raw SQL / bypass-policy MCP tools

### 4.4 Extension points on current codebase

```text
synapsemd_platform/
  api/routes/cases.py          # NEW
  services/command_orchestrator.py   # branch CASE_COMMANDS
  mcp/dispatch.py + tools_case.py    # NEW tools
  auth/roles.py                      # operational roles/scopes
  case_management/                   # NEW package (Procedure Layer)
  artifact_registry/                 # NEW package (Artifact Layer services)
  agents/                            # NEW Pydantic AI agent factories
```

### 4.5 Pydantic AI on the Platform Layer

Platform hosts Pydantic AI so every agent run:

1. Resolves **model** via existing `ModelPolicyEngine` (not hard-coded vendor keys in agents).
2. Injects **dependencies** (`RunContext[CaseDeps]`): tenant_id, user_id, case_id, scopes, consent flags, DB session factories.
3. Restricts **tools** to allowlisted functions that call `CaseService` / read-only queries — never direct gate bypass.
4. Emits **OTel / Logfire** spans with tenant_id, case_id, artifact versions, model_id — **no PHI** in spans.
5. Validates **structured output** with Pydantic models (compile drafts, advice payloads, specialist opinions).

References: [Pydantic AI Agents](https://ai.pydantic.dev/), [GitHub pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai), [Pydantic stack](https://pydantic.dev/).

Illustrative pattern (design intent, not production code):

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

@dataclass
class CaseDeps:
    tenant_id: str
    user_id: str
    case_id: str
    scopes: frozenset[str]

class AdviceOutput(BaseModel):
    summary: str
    gaps: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    recommended_human_actions: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)

advice_agent = Agent(
    "openai:gpt-4o",  # resolved at runtime via ModelPolicyEngine → provider string
    deps_type=CaseDeps,
    output_type=AdviceOutput,
    instructions="Advise only. Never claim room release or clinical diagnosis.",
)

@advice_agent.tool
async def get_case_snapshot(ctx: RunContext[CaseDeps]) -> dict:
    """Read-only case + open tasks + missing evidence summary."""
    ...
```

Optional later: [Temporal durable execution](https://ai.pydantic.dev/) for long-running compile or multi-step advice jobs — still subordinate to CaseService for state writes.

---

## 5. The Artifact Layer

### 5.1 Role

The Artifact Layer is the **versioned knowledge and control plane**: everything an auditor can point to as “what procedure was in force.”

Git remains the **authoring** source. The **Artifact Registry** in Postgres is the **runtime authority**.

### 5.2 Artifact types

| Type | Purpose | Example |
|------|---------|---------|
| `CASE_PLAYBOOK` | Case type intent, mode, goals, state list, step refs | `terminal-isolation-cleaning@1.0` |
| `POLICY` | Deterministic gates (SoD, release, contact-time, competency) | `room-release-gate@1.0` |
| `TASK_TEMPLATE` | Checklist / form schema for a step | `HKP-FRM-001A` |
| `EVENT_CATALOG` | Allowed event names + schemas | Appendix E |
| `ISOLATION_PROFILE` | PPE, disinfectant, contact time, IPC flags | Contact / Airborne variants |
| `COMMAND` | Thin user/API verbs | `case`, `case-task`, `case-release` |
| `SKILL` | Advisory / analysis playbooks | evidence-completeness, KPI pack |
| `SPECIALIST` | Review personas (not executors) | IPC, Quality, Facility Engineering |
| `AGENT_SPEC` | Pydantic AI agent definition (instructions, tools allowlist, output schema id, model tier) | `sop-compiler`, `cleaning-compliance-advisor` |

### 5.3 Authoring layout (repo)

```text
case-playbooks/
  terminal-isolation-cleaning/
    CASE.md
    procedure.yaml
    events.yaml
    profiles/
    task-templates/
    policies/
commands/
  case.md
  case-task.md
  case-release.md
skills/
  cleaning-evidence-completeness/
  sop-effectiveness-kpi/
specialists/
  infection-control.md
  quality-assurance.md
  facility-engineering.md
agents/                          # Pydantic AI specs (YAML/JSON or Python factories)
  specs/
    sop-compiler.yaml
    case-advisor.yaml
    specialist-ipc.yaml
```

### 5.4 Registry lifecycle

```text
DRAFT → REVIEW → APPROVED → ACTIVE → RETIRED
```

Rules:

- Tier 1 (e.g. HKP-SOP-001): Clinical/IPC + Quality + system assurance sign-off before `ACTIVE`.
- Cases store `artifact_versions` map + content hashes at creation.
- Superseded versions remain readable for reconstruction (ROM-SOP-007 / HKP §19–20).
- Platform never loads “latest git file” in production; it loads `ACTIVE` registry rows.

### 5.5 Registry schema (logical)

```text
artifact_registry
  artifact_id, artifact_type, name, version
  content_hash, storage_uri
  status, risk_class, sop_code, sop_version
  owner, approved_by, effective_from, effective_to
  tenant_scope, source_commit
  agent_spec_ref (optional)   # for AGENT_SPEC / linked advisors
```

### 5.6 Relationship to existing command catalog

Today `PLATFORM_COMMANDS` in `models/commands.py` seeds `command_catalog`. Artifact Layer **extends** that pattern:

- Keep a small set of platform-registered commands (`case`, `case-task`, `case-inspect`, `case-release`, …).
- Do **not** register one command per SOP step.
- Skills / specialists remain markdown; runtime may store hashes in registry without requiring Python edits for SME content (platform rails still enforce promotion).

---

## 6. The Procedure Layer (CASE plane)

### 6.1 Role

The Procedure Layer is the **CASE plane**: create and advance cases, enforce gates, journal events, drive twin/integration updates, and **assist generation of Artifact Layer drafts from SOPs**.

It has two faces:

| Face | Mode | Description |
|------|------|-------------|
| **Runtime** | `PROCEDURE_BOUND` (primary) / later `ADAPTIVE` | Execute pinned playbooks |
| **Compile** | Offline / governed pipeline | SOP → draft artifacts → human promote |

### 6.2 Orchestration modes

**PROCEDURE_BOUND** (HKP-SOP-001 class):

- Fixed state machine (SOP §6.2) + step graph (SOP §7).
- Next transitions from compiled procedure + GateEngine.
- Mandatory tasks, timers, SoD, release gate.
- Agents advise; humans execute; platform enforces.

**ADAPTIVE** (later; SYN-ARCH-DCM-001):

- Goals + events + case plan versions.
- Case Intelligence recommends; policies still constrain.
- Same aggregate tables; different engine path.

### 6.3 Case aggregate

```text
Case
  case_id, tenant_id
  case_type, orchestration_mode
  status / procedure_state
  subject { type: room_twin | patient | ..., id }
  pinned: playbook, policies, templates, sop_code/version
  participants[], assignments[]
  tasks[], evidence[], decisions[], recommendations[]
  escalations[], milestones[], events[]
  version (optimistic concurrency)
```

### 6.4 Core engines

| Engine | Responsibility |
|--------|----------------|
| **CaseService** | Lifecycle, concurrency, load aggregate |
| **TaskEngine** | Instantiate templates × profile; accept/complete/reopen |
| **GateEngine** | Deterministic allow/deny with reason_codes |
| **AssignmentEngine** | Role/queue + competency checks |
| **SLA / EscalationEngine** | Section 16 timers and L1/L2/L3 |
| **TwinService** | Room Twin readiness / restriction |
| **OutboxPublisher** | Bed Mgmt, notifications, integrations |
| **AdviceEngine** | Invokes Pydantic AI advisors; writes `recommendations` only |
| **SopCompilerService** | Invokes compile agents; writes **DRAFT** artifacts only |

### 6.5 Deterministic gates (examples for HKP-SOP-001)

| Gate ID | Enforces |
|---------|----------|
| `pre_entry` | PPE + supplies complete |
| `contact_time` | Product contact timer elapsed |
| `sod_inspection` | inspector ≠ cleaner |
| `evidence_complete` | Mandatory evidence present |
| `competency` | Assignee competency valid |
| `release` | Appendix D prerequisites |
| `no_ai_release` | Approver must be human role with scope |

Gate evaluation returns structured policy decisions (same spirit as DCM policy outputs): `ALLOW | DENY | REQUIRE_REVIEW` + reason_codes + required_actions.

### 6.6 Event model

Immutable `case_events` + transactional `outbox_events` (Postgres first; Kafka later).

Ingress examples (HKP Appendix E): `room.vacated`, `isolation.context.confirmed`, `cleaning.task.completed`, `cleaning.inspection.failed`, `room.release.approved`, …

Idempotency: duplicate trigger detection before second case create for same room+trigger window.

### 6.7 Procedure Layer → Artifact Layer generation

The Procedure Layer **does not** silently publish production playbooks. It runs a **governed compile pipeline**:

```text
┌─────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│ SOP source  │────►│ SopCompilerService   │────►│ DRAFT artifacts │
│ PDF/DMS/JSON│     │ + Pydantic AI agents │     │ in registry     │
└─────────────┘     └──────────────────────┘     └────────┬────────┘
                                                          │
                     ┌──────────────────────┐             │
                     │ Human review UI/API  │◄────────────┘
                     │ Quality / IPC / SME  │
                     └──────────┬───────────┘
                                │ approve
                                ▼
                     ┌──────────────────────┐
                     │ ACTIVE artifacts     │
                     │ Artifact Layer       │
                     └──────────────────────┘
```

**Compiler outputs (typed):**

1. `CASE_PLAYBOOK` draft (states, goals, step references)
2. `POLICY` drafts (SoD, release, timers) extracted from SOP tables
3. `TASK_TEMPLATE` drafts from forms / 7-column procedure
4. `EVENT_CATALOG` draft
5. `ISOLATION_PROFILE` drafts where present
6. Suggested `AGENT_SPEC` stubs (advisor + specialist) — still DRAFT
7. Gap report: sections missing vs ROM-SOP-007 / DoD gate

**Hard rules:**

- Compiler output type is a Pydantic model (e.g. `CompiledSopBundle`).
- Schema validators reject incomplete Tier-1 mandatory sections.
- No `ACTIVE` transition without human approval chain.
- AI model/prompt changes that affect compile are **major change control** (HKP §20).

---

## 7. Pydantic AI — Dynamic Agent Architecture

### 7.1 Why Pydantic AI

Chosen for SynapseMD agent work because it provides ([docs](https://ai.pydantic.dev/), [repo](https://github.com/pydantic/pydantic-ai)):

- **Typed agents** — structured outputs and tool args validated with Pydantic (already core to FastAPI stack).
- **Dependency injection** — tenant/case/auth context without globals.
- **MCP capability** — agents can attach to SynapseMD MCP as clients for allowlisted tools.
- **Composable capabilities** — MCP, tools, instructions bundled; Harness optional for advanced coding/compile workspaces.
- **Observability** — OpenTelemetry-native; Logfire optional.
- **Evals** — [Pydantic Evals](https://pydantic.dev/) for release gates on advisor/compiler behavior.
- **Durable execution (optional)** — Temporal/DBOS/Prefect for long compile jobs.

### 7.2 Agent classes (dynamic creation model)

Agents are **created from `AGENT_SPEC` artifacts** (or Python factories registered by name), not invented ad hoc by another agent at production runtime.

| Agent class | Created when | Tools | Output | May write case state? |
|-------------|--------------|-------|--------|------------------------|
| **SopCompilerAgent** | Compile job for SOP code | Read SOP blob, emit structured bundle | `CompiledSopBundle` | No — only DRAFT registry via CompilerService |
| **CaseAdvisorAgent** | On `recommend` / SLA risk / evidence gap | Read-only case snapshot tools | `AdviceOutput` | No — recommendations only |
| **SpecialistReviewAgent** | IPC / Quality consult | Read case + evidence summaries | `SpecialistOpinion` | No — opinion → decision only after human |
| **ComplianceAnalystAgent** | KPI / audit assist | Aggregates, no PHI dumps | `ComplianceReport` | No |
| **CoordinatorAgent** (optional) | Summarize open blockers | Read-only | `CoordinatorBrief` | No |

**Dynamic creation** means:

```text
AGENT_SPEC (registry)
  + ModelPolicyEngine decision
  + CaseDeps / CompileDeps
  + allowlisted toolset for that spec
  → Pydantic AI Agent instance (ephemeral or cached)
```

It does **not** mean: “LLM discovers arbitrary MCP tools and spawns privileged agents.”

### 7.3 Tool allowlists

| Tool surface | Allowed callers |
|--------------|-----------------|
| `get_case`, `get_case_tasks`, `get_case_evidence` | Advisors, specialists |
| `recommend_case_actions` (writes recommendation row via service) | Advisors |
| `complete_case_task`, `approve_release` | **Humans / system with scopes only** — not agent toolsets |
| `create_draft_artifacts` | CompilerService after validating `CompiledSopBundle` |
| External MCP (HIMS, Bed Mgmt) | Platform adapters; agents use platform tools that wrap adapters |

### 7.4 Agent factory (design)

```text
agents/
  factory.py          # build_agent(spec_id, deps) -> Agent
  specs/              # YAML AGENT_SPEC
  tools/
    case_readonly.py
    compile_tools.py
  outputs/
    advice.py
    compiled_sop.py
    specialist.py
```

`build_agent`:

1. Load `AGENT_SPEC` from Artifact Registry (ACTIVE or job-scoped DRAFT for compile).
2. Resolve model via Platform `ModelPolicyEngine`.
3. Attach instructions from specialist/skill markdown (hashed).
4. Register only tools listed in spec.
5. Set `output_type` from registered Pydantic model.
6. Optionally attach `MCP(...)` capability pointing at **SynapseMD MCP** with a constrained token (read scopes).

### 7.5 Relationship to CommandOrchestrator and MDT

| Path | Today | Future |
|------|-------|--------|
| Health commands | `HealthDataService` | Unchanged |
| AI Module 21 | `AIService` | Unchanged |
| LLM consult / specialist MDT | `workers/specialist.py` + LLMOrchestrator | Migrate specialist fan-out to **Pydantic AI SpecialistReviewAgent** (same prompts, typed outputs) |
| Case advice | — | Pydantic AI CaseAdvisorAgent |
| SOP compile | — | Pydantic AI SopCompilerAgent |

Guardrails remain: MedicalGuardrails on free-text; structured outputs additionally schema-validated.

### 7.6 Evals and release gates

Before promoting an `AGENT_SPEC` to ACTIVE:

- Golden SOP snippets → expected `CompiledSopBundle` fields (Pydantic Evals).
- Adversarial prompts: attempt to release room / skip SoD → must refuse / produce no mutating tool calls.
- PHI leakage tests on traces and outputs.

---

## 8. End-to-End Flows

### 8.1 Compile flow (Procedure → Artifact)

```text
1. Ingest SOP (upload / DMS hook) → object store + metadata
2. SopCompilerService starts job (audit: sop.compile.started)
3. SopCompilerAgent.run(sop_text_or_structured) → CompiledSopBundle
4. Schema + Tier applicability validators
5. Persist DRAFT playbook/policies/templates/agent_specs
6. Notify reviewers (Quality, IPC, Function Head)
7. Approvals recorded (no self-approval)
8. Promote ACTIVE; withdraw prior if major
9. Train/attest trigger (HKP §18) — out of band LMS
```

### 8.2 Runtime flow (PROCEDURE_BOUND)

```text
1. Event room.vacated (MCP/API)
2. CaseService.create — pin ACTIVE artifacts; instantiate tasks from profile
3. Twin blocked; Bed Mgmt notified (outbox)
4. AssignmentEngine assigns competent staff
5. Humans: accept task → complete with evidence (gates on each transition)
6. Optional: CaseAdvisorAgent flags gaps (recommendation only)
7. Supervisor inspection decision (SoD gate)
8. IPC / engineering if required
9. Human release approve (no_ai_release)
10. Twin READY; notify; close when closure gate passes
11. KPI emission / effectiveness hooks
```

### 8.3 Advice flow

```text
Human or SLA worker → recommend_case_actions
  → AdviceEngine → CaseAdvisorAgent (Pydantic AI)
  → Guardrails + schema
  → case_recommendations row + optional review_queue
  → Human acts via case-task / case-inspect / case-release
```

---

## 9. MCP Adapters

### 9.1 SynapseMD MCP (platform-owned)

Extends current `synapsemd-mcp` with case tools:

```text
create_case, get_case, search_cases
get_case_tasks, complete_case_task, add_case_evidence
add_case_event, get_case_events
request_case_review, escalate_case, close_case
recommend_case_actions
get_room_twin
compile_sop_preview          # returns draft bundle; does not AUTO-ACTIVE
list_artifacts, get_artifact
```

**Forbidden:** `skip_gate`, `set_database_state`, `execute_sql`, `approve_release` without human JWT + role.

### 9.2 External MCP servers

Integrations (HIMS, Bed Management, Inventory, BMS, DMS) may be separate MCP servers. Platform adapters call them; case agents call **platform** tools only. This keeps SoD and audit in one place.

### 9.3 UI clients

AnythingLLM / Open WebUI attach to SynapseMD MCP as today ([docs/ui-mcp-integration.md](../docs/ui-mcp-integration.md)). Pydantic AI agents may also be MCP clients with **narrower** tokens than human admins.

---

## 10. Commands, Skills, Specialists (mapping)

| Artifact | Role in this architecture |
|----------|---------------------------|
| **Commands** | Thin verbs: create/show/task/inspect/release/escalate/reconcile/compile |
| **Skills** | Analysis playbooks invoked by advisor agents or CLI |
| **Specialists** | Instruction packs for SpecialistReviewAgent |
| **Playbooks / Policies / Templates** | PROCEDURE_BOUND execution fuel |
| **AGENT_SPEC** | How Pydantic AI agents are dynamically constructed |

RACI **Responsible** roles (e.g. Housekeeping Staff) are **human assignees**, not LLM specialists.

---

## 11. Data Model (Procedure + Artifact)

### 11.1 New schemas (logical)

```text
artifact_registry, artifact_approvals
cases, case_participants, case_tasks, case_evidence
case_decisions, case_recommendations, case_events
case_escalations, case_approvals
outbox_events
room_twins (or adapter projection)
sop_compile_jobs
agent_runs (interaction metadata; no PHI prompts in clear logs)
```

### 11.2 RLS

All tenant-scoped tables registered in `core/rls.py` alongside existing `review_queue`, etc.

### 11.3 Audit event types (additive)

```text
sop.compile.started|completed|failed
artifact.draft.created|artifact.promoted|artifact.retired
case.created|case.task.completed|case.gate.denied
case.recommendation.generated
case.release.approved|rejected
case.closed|case.reconciled
agent.run.started|completed   # model_id, spec_id, hashes only
```

---

## 12. Package Design (on current codebase)

```text
platform/synapsemd_platform/
  case_management/           # Procedure Layer runtime
    domain/
    models/
    services/
    engines/
    adapters/
    workers/
  artifact_registry/         # Artifact Layer services
    models/
    promote.py
    loaders.py
  agents/                    # Pydantic AI
    factory.py
    specs/
    tools/
    outputs/
  api/routes/cases.py
  api/routes/artifacts.py
  mcp/tools_case.py
```

Repo authoring roots (unchanged philosophy):

```text
case-playbooks/  commands/  skills/  specialists/  agents/specs/
```

Dependency: add `pydantic-ai` to `platform/pyproject.toml` (alongside existing `pydantic` / `mcp`). Optional extras: `pydantic-evals`, Logfire, Temporal when needed.

---

## 13. Security, Compliance, and Clinical/Operational Safety

1. **SoD** enforced in GateEngine + DB constraints, not prompts.
2. **Minimum necessary** context to agents; anonymize when patient-linked.
3. **No training** on tenant PHI without separate approval (HKP §11).
4. **Downtime mode**: degraded case + paper forms + reconcile command (HKP §15).
5. **Change control**: major SOP / AI prompt / agent-spec changes require Tier-appropriate approval (HKP §20, ROM-SOP-007).
6. **Traceability chain:** SOP version → playbook → case → task → evidence → decision → twin → KPI.
7. **Agent evals** required before ACTIVE `AGENT_SPEC`.

---

## 14. Delivery Phases

| Phase | Scope | Exit criteria |
|-------|--------|----------------|
| **F0** | Schema: cases, tasks, evidence, events, outbox, artifact_registry + RLS | Migrations green |
| **F1** | CaseService + GateEngine + REST + orchestrator `case*` branch | PROCEDURE_BOUND create→task→blocked release without approval |
| **F2** | Hand-compiled HKP-SOP-001 ACTIVE artifacts | Closed case pins SOP/playbook versions |
| **F3** | MCP case tools + Room Twin stub | UI can observe; cannot release via agent token |
| **F4** | Pydantic AI CaseAdvisorAgent + factory + evals | Advice-only; FAQ 23.4 tests pass |
| **F5** | SopCompilerAgent → DRAFT artifacts + human promote API | No auto-ACTIVE |
| **F6** | SLA/escalation workers, downtime reconcile | §15–16 behaviors tested |
| **F7** | Specialist agents migrate from `workers/specialist.py` | Typed opinions + audit |
| **F8** | Optional ADAPTIVE mode | Isolated by `orchestration_mode` |

---

## 15. Explicit Non-Goals

- BPMN designer as a product requirement for v1
- LLM-generated unrestricted workflows in production
- Agents that self-approve Tier-1 release
- Hot-swapping ACTIVE playbooks under open cases
- Parallel identity/audit stacks
- One command-catalog entry per SOP procedure row
- Runtime “agent reads PDF and invents tools”

---

## 16. Worked Example — HKP-SOP-001

| SOP element | Layer | Artifact / runtime |
|-------------|-------|-------------------|
| §6.2 states | Artifact → Procedure | `procedure.yaml` states |
| §7 forty steps | Artifact | Task templates + graph |
| §8 SoD | Artifact Policy | `sod_inspection`, `no_ai_release` |
| §14 KPIs | Skill + analytics | ComplianceAnalystAgent |
| Appendix B profiles | Artifact | `ISOLATION_PROFILE` |
| Appendix D release gate | GateEngine | `release` policy |
| Appendix E events | Event catalog | Ingress/outbox names |
| FAQ 23.4 | Agent policy | Advisor tools exclude approve_release |
| Room Twin | TwinService + MCP | subject + readiness |

**Compile:** Procedure Layer SopCompilerAgent drafts the above from SOP → humans promote → Artifact Layer ACTIVE → Runtime pins on each terminal-cleaning case.

---

## 17. Summary Diagram (all three layers + Pydantic AI)

```text
                 ┌────────────────────────────┐
                 │   SOP (controlled DMS)     │
                 └─────────────┬──────────────┘
                               │
                 ┌─────────────▼──────────────┐
                 │ PROCEDURE LAYER            │
                 │ SopCompiler (Pydantic AI)  │
                 │ Case Runtime + GateEngine  │
                 │ Advice agents (Pydantic AI)│
                 └──────┬───────────┬─────────┘
            drafts│           │runtime
                 ┌▼───────────▼─────────┐
                 │ ARTIFACT LAYER       │
                 │ Registry ACTIVE pin  │
                 │ Playbook·Policy·Task │
                 │ Skill·Specialist·Spec│
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │ PLATFORM LAYER       │
                 │ Trust · MCP · Audit  │
                 │ ModelPolicy · RLS    │
                 │ Hosts Pydantic AI    │
                 └──────────────────────┘

Pipeline:
SOP → compiled Playbook+Policies+Templates → Case Runtime (gates)
    → MCP adapters → humans execute, agents advise, platform enforces
```

---

## 18. Document Control

| Field | Value |
|-------|--------|
| Document ID | SYN-ARCH-SOP-CASE-001 |
| Version | 0.1 Draft |
| Supersedes | — (complements SYN-ARCH-DCM-001; does not replace enterprise ENT-001) |
| Next review | After F2 (HKP-SOP-001 vertical) or major Pydantic AI integration decision |

**References**

- [Pydantic AI on GitHub](https://github.com/pydantic/pydantic-ai)
- [Pydantic AI documentation](https://ai.pydantic.dev/)
- [Pydantic — AI engineering stack](https://pydantic.dev/)
- SynapseMD Dynamic Case Management Architecture (`SYN-ARCH-DCM-001`)
- HKP-SOP-001 — Terminal Cleaning of Isolation Room
- ROM-SOP-007 — SOP on SOP
