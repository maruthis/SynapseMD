# **SynapseMD Dynamic Case Management —

Enterprise Architecture and Design**

**Document ID:** SYN-ARCH-DCM-001  
**Status:** Draft Architecture & Design Proposal  
**Date:** 2026-08-17  
**Audience:** Engineering, Architecture, Security, Compliance, Product, Clinical SMEs  
**Companion Architecture:** SynapseMD Enterprise Platform — Architecture and Design (SYN-ARCH-ENT-001)

# 1\. Executive Summary

SynapseMD Dynamic Case Management (DCM) introduces a **goal-driven, event-driven, intelligence-assisted case orchestration capability** into the SynapseMD Enterprise Platform.

It is deliberately **not a BPMN workflow engine**.

Traditional workflow platforms assume that the process can be substantially predefined:

Start → Activity → Decision → Activity → End

Dynamic Case Management addresses a different problem.

A healthcare case continuously evolves as new information becomes available:

- laboratory results,
- diagnoses,
- medication changes,
- specialist opinions,
- patient-reported information,
- social determinants,
- missed appointments,
- alerts,
- risk changes,
- external events,
- care-plan updates,
- regulatory or organizational policies.

The appropriate next action therefore cannot always be predetermined.

Instead, SynapseMD DCM continuously evaluates:

**Given the current case state, goals, evidence, risks, policies, available skills, specialist expertise, and new events, what should happen next?**

The architecture extends SynapseMD's existing philosophy:

**Domain stays artifact-driven; platform owns trust, execution, distribution, persistence, governance, and scale.**

The Dynamic Case Management platform therefore separates:

Technical Platform  
+  
Case Runtime  
+  
Domain Knowledge  
+  
Deterministic Intelligence  
+  
AI-assisted reasoning  
+  
Human Decision Making

Domain knowledge remains extensible through human-readable artifacts:

Commands  
Skills  
Specialists  
Policies  
Case Playbooks

while the technical case-management runtime remains domain-independent.

This allows SynapseMD to support:

Personal Health  
↓  
Clinical Assistant  
↓  
Hospital Case Management  
↓  
Enterprise Care Coordination  
↓  
Multi-organization Healthcare Network

without changing the fundamental architecture.

The same case engine can eventually support other domains such as insurance claims, legal matters, government services, compliance investigations, and HR cases simply by replacing domain artifacts.

# 2\. Architectural Vision

The core architectural vision is:

**A Case is not a predefined workflow instance. A Case is a continuously evolving body of goals, evidence, participants, risks, decisions, tasks, events, and outcomes managed under defined policies.**

SynapseMD DCM therefore uses:

Goals  
+  
Events  
+  
Evidence  
+  
Policies  
+  
Skills  
+  
Specialists  
+  
Deterministic Rules  
+  
AI Recommendations  
+  
Human Decisions

rather than BPMN process definitions.

# 3\. Relationship to Existing SynapseMD Enterprise Architecture

The existing Enterprise Platform architecture establishes:

- PostgreSQL as enterprise system of record.
- OIDC SSO and MFA.
- RBAC + ABAC.
- tenant-level PostgreSQL RLS.
- OpenTelemetry.
- durable, tamper-evident auditing.
- PHI anonymization.
- policy-driven model selection.
- explicit consent.
- Commands / Skills / Specialists remaining artifact-driven.

Dynamic Case Management inherits all of these requirements.

It **must not create parallel implementations** of:

- identity,
- authorization,
- PHI handling,
- LLM routing,
- audit,
- logging,
- consent,
- object storage,
- FHIR,
- secrets management,
- model selection.

Instead, DCM becomes another enterprise subsystem running on the same trust architecture.

# 4\. Architectural Principles

## 4.1 Case-first, not process-first

Do not model the patient journey as:

workflow_step = 6

Instead model independent dimensions:

Clinical risk = HIGH  
Medication review = REQUIRED  
Renal monitoring = ACTIVE  
Social assessment = IN_PROGRESS  
Patient engagement = AT_RISK  
Cardiology consult = RECOMMENDED

Multiple aspects of a case can evolve simultaneously.

## 4.2 Goal-driven orchestration

Every case should have explicit desired outcomes.

Example:

goals:  
\- id: stabilize-glycemic-control  
priority: high  
status: active  
<br/>\- id: prevent-renal-deterioration  
priority: critical  
status: active  
<br/>\- id: improve-medication-adherence  
priority: high  
status: at-risk

The system continuously evaluates:

Current State  
+  
Goals  
+  
Evidence  
+  
Policies  
+  
Domain Intelligence  
↓  
Potential Next Actions

## 4.3 Deterministic-first

LLMs must not own critical workflow decisions.

Deterministic logic should control:

- safety rules,
- mandatory escalations,
- authorization,
- consent,
- SLA timers,
- eligibility,
- task completion criteria,
- case closure,
- policy enforcement,
- approval requirements,
- high-risk clinical thresholds.

LLMs may assist with:

- summarization,
- synthesis,
- prioritization,
- relevant skill discovery,
- specialist selection,
- option generation,
- missing-information detection,
- multidisciplinary reasoning,
- patient communication.

This follows SynapseMD's existing architecture in which Module 21 remains deterministic and generative AI may provide a narrative overlay only after controlled scoring.

## 4.4 Domain independence

The core engine must never contain code such as:

if diabetes_case:  
...

The runtime understands only generic concepts:

Case  
Goal  
Problem  
Risk  
Task  
Event  
Milestone  
Evidence  
Decision  
Recommendation  
Policy  
Participant  
Assignment  
Plan  
Review

Healthcare-specific behavior lives in artifacts.

## 4.5 Artifact-driven intelligence

SynapseMD already requires that Commands, Skills, and Specialists remain Markdown-driven even in enterprise mode.

DCM extends the model to:

commands/  
skills/  
specialists/  
policies/  
case-playbooks/

The technical platform executes and constrains these artifacts.

## 4.6 AI proposes; policy constrains; humans decide

For consequential actions:

AI Recommendation  
↓  
Policy Evaluation  
↓  
Safety Validation  
↓  
Human Review  
↓  
Approved Action

No LLM should autonomously:

- prescribe,
- discharge,
- close high-risk cases,
- override policies,
- bypass consent,
- alter observed facts,
- approve itself.

# 5\. Conceptual Architecture

┌────────────────────────────────────────────────────────────┐  
│ EXPERIENCE LAYER │  
│ │  
│ CLI │ IDE │ AnythingLLM │ Open WebUI │ PWA │ Partner Apps │  
└──────────────────────────────┬─────────────────────────────┘  
│  
API Gateway / WAF  
│  
▼  
┌────────────────────────────────────────────────────────────┐  
│ SYNAPSEMD ENTERPRISE PLATFORM │  
│ │  
│ Identity │ Authorization │ Consent │ Orchestrator │ Audit │  
│ │  
│ DYNAMIC CASE MANAGEMENT │  
│ │  
│ Case Service │  
│ Case Intelligence Engine │  
│ Goal Engine │  
│ Task Engine │  
│ Event Engine │  
│ Policy Engine │  
│ Milestone Engine │  
│ SLA / Escalation Engine │  
│ Assignment Engine │  
│ Recommendation Engine │  
│ Human Review │  
│ Case Coordinator │  
│ │  
│ Module 21 │ PHI Service │ Model Policy │ Guardrails │ RAG │  
└───────────────────────┬────────────────────────────────────┘  
│  
┌───────────────┼────────────────┐  
▼ ▼ ▼  
HealthDataService CaseDataService Artifact Registry  
│ │ │  
└───────────────┼────────────────┘  
▼  
PostgreSQL  
System of Record + RLS  
│  
┌────────────────┼─────────────────┐  
▼ ▼ ▼  
Object Store FHIR Projection Audit/WORM

# 6\. Logical Component Architecture

## 6.1 Case Service

Primary application service for case lifecycle management.

Responsibilities:

- create case,
- retrieve case,
- update case metadata,
- assign participants,
- suspend/reopen case,
- initiate closure,
- load current aggregate state,
- enforce optimistic concurrency,
- invoke case policy checks.

It should not contain domain-specific clinical reasoning.

## 6.2 Case Intelligence Engine

The core adaptive intelligence component.

Responsibilities:

Observe  
Assess  
Identify  
Recommend  
Coordinate  
Re-evaluate

It evaluates:

- current case state,
- new events,
- active goals,
- problems,
- risks,
- evidence,
- active tasks,
- applicable policies,
- relevant skills,
- specialist expertise,
- previous decisions,
- milestones,
- incomplete information.

Output:

Candidate Case Actions

not direct execution.

## 6.3 Goal Engine

Responsible for:

- goal creation,
- goal state evaluation,
- goal dependencies,
- goal progress,
- goal breach,
- goal completion,
- goal conflict,
- goal prioritization.

Suggested statuses:

PROPOSED  
ACTIVE  
ON_TRACK  
AT_RISK  
BLOCKED  
ACHIEVED  
ABANDONED  
SUPERSEDED

## 6.4 Task Engine

Tasks represent executable units of work.

Examples:

- clinician review,
- patient contact,
- repeat lab,
- medication reconciliation,
- social worker assessment,
- schedule appointment,
- specialist consult.

Task state:

PROPOSED  
READY  
ASSIGNED  
IN_PROGRESS  
BLOCKED  
COMPLETED  
CANCELLED  
FAILED  
EXPIRED

Tasks may be:

Human  
System  
AI-assisted  
External-system

## 6.5 Event Engine

Events trigger re-evaluation.

Examples:

case.created  
case.updated  
<br/>lab.received  
observation.received  
condition.changed  
medication.changed  
<br/>goal.created  
goal.at_risk  
goal.completed  
<br/>task.created  
task.completed  
task.overdue  
<br/>appointment.missed  
<br/>risk.increased  
<br/>specialist.review.completed  
<br/>case.escalated  
case.closed

Events are immutable.

# 7\. Event-Driven Architecture

Dynamic Case Management should use a transactional event model.

## V1

PostgreSQL  
+  
Case Event Journal  
+  
Transactional Outbox  
+  
Background Worker

No Kafka dependency is required initially.

## Enterprise scale

Case Transaction  
│  
├── Case State  
├── Case Event  
└── Outbox Event  
│  
▼  
Outbox Publisher  
│  
▼  
Kafka  
┌─────┼──────────────┐  
▼ ▼ ▼  
Case Worker Notification Analytics

This preserves SynapseMD's principle of starting small while providing an enterprise scaling path.

# 8\. Transactional Outbox

Every material state change should atomically write:

Business Update  
+  
Case Event  
+  
Outbox Record

Example:

BEGIN;  
<br/>UPDATE case_management.case_goals  
SET status = 'AT_RISK'  
WHERE goal_id = :goal_id;  
<br/>INSERT INTO case_management.case_events (...);  
<br/>INSERT INTO platform.outbox_events (...);  
<br/>COMMIT;

This prevents:

DB committed  
but  
event publication failed

and avoids distributed transaction complexity.

# 9\. Case Aggregate

A Case is the aggregate root.

Conceptual canonical representation:

{  
"case_id": "CASE-2026-001239",  
"tenant_id": "TENANT-001",  
<br/>"case_type": "complex-diabetes-management",  
<br/>"status": "ACTIVE",  
<br/>"subject": {  
"type": "patient",  
"id": "PAT-001"  
},  
<br/>"priority": "HIGH",  
<br/>"goals": \[\],  
<br/>"problems": \[\],  
<br/>"risks": \[\],  
<br/>"participants": \[\],  
<br/>"assignments": \[\],  
<br/>"tasks": \[\],  
<br/>"milestones": \[\],  
<br/>"recommendations": \[\],  
<br/>"decisions": \[\],  
<br/>"events": \[\],  
<br/>"evidence": \[\],  
<br/>"case_plan": {},  
<br/>"reviews": \[\],  
<br/>"escalations": \[\],  
<br/>"active_policies": \[\],  
<br/>"skills": \[\],  
<br/>"specialists": \[\],  
<br/>"artifact_versions": {},  
<br/>"version": 12  
}

# 10\. Case Lifecycle

Recommended generic lifecycle:

DRAFT  
│  
▼  
OPEN  
│  
▼  
ACTIVE  
│  
├────► ON_HOLD  
│ │  
│ └──► ACTIVE  
│  
├────► ESCALATED  
│ │  
│ └──► ACTIVE  
│  
▼  
RESOLUTION_PENDING  
│  
▼  
CLOSED

Optional:

CANCELLED  
MERGED  
TRANSFERRED

Lifecycle transitions are deterministic and policy-controlled.

# 11\. Case Plans

Unlike BPMN, a Case Plan is not a fixed execution graph.

It represents:

**The current agreed set of actions intended to progress the case toward its goals.**

Example:

Case Plan v4  
<br/>Goal: Improve glycemic control  
<br/>Actions:  
1\. Review medication adherence  
2\. Analyze CGM trend  
3\. Schedule endocrinology review  
4\. Conduct nutrition assessment  
5\. Repeat HbA1c after agreed interval

New evidence may generate:

Case Plan v5

instead of mutating v4.

# 12\. Case Plan Versioning

Tables:

case_plans  
case_plan_versions  
case_plan_actions

Every version should preserve:

trigger_event_id  
generated_by  
approved_by  
skills_used  
specialists_used  
policies_applied  
model_id  
model_policy_decision  
evidence_ids  
reason_codes  
created_at

This provides longitudinal explainability.

# 13\. Evidence Model

Evidence must be a first-class object.

Types may include:

OBSERVATION  
CONDITION  
MEDICATION  
DOCUMENT  
PATIENT_STATEMENT  
SPECIALIST_REVIEW  
SKILL_RESULT  
MODULE21_RESULT  
POLICY  
EXTERNAL_EVENT  
TASK_RESULT

Reasoning lineage becomes:

Evidence  
↓  
Derived Assessment  
↓  
Recommendation  
↓  
Decision  
↓  
Action

# 14\. Semantic Separation: Fact vs Derivation vs Recommendation

The data model must distinguish:

### Observed Fact

HbA1c = 9.2

### Derived Assessment

Glycemic control has worsened

### Recommendation

Consider endocrinology review

### Human Decision

Endocrinology review approved

These must not be stored as interchangeable values.

Recommended entity classes:

case_evidence  
case_assessments  
case_recommendations  
case_decisions

LLMs may create recommendations.

They must never overwrite original evidence.

# 15\. Case Participants

Participants may be:

Patient  
Caregiver  
Physician  
Nurse  
Case Manager  
Social Worker  
Dietitian  
Pharmacist  
Specialist  
Organization  
AI Specialist  
External Service

Participation should have:

participant_type  
participant_id  
role  
valid_from  
valid_until  
permissions  
assignment_scope

# 16\. Assignment Engine

Assignments should support:

Individual  
Role  
Team  
Queue  
Organization

Example:

Task: Medication reconciliation  
<br/>Assignment:  
role = clinical_pharmacist  
team = diabetes-care-team

Rather than hard-wiring users.

Assignment rules can consider:

Case type  
Patient location  
Specialty  
Tenant  
Workload  
Availability  
Priority  
SLA

# 17\. Milestone Engine

Milestones represent significant state achievements.

Examples:

INITIAL_ASSESSMENT_COMPLETE  
BASELINE_LABS_COMPLETE  
CARE_PLAN_APPROVED  
MULTIDISCIPLINARY_REVIEW_COMPLETE  
PATIENT_EDUCATION_COMPLETE  
FOLLOWUP_COMPLETE  
CASE_READY_FOR_CLOSURE

Milestones may be:

- automatically evaluated,
- manually confirmed,
- policy mandated.

# 18\. SLA and Timer Architecture

Do not use BPMN timers.

Model timers explicitly:

case_sla_definitions  
case_sla_instances  
case_deadlines

Examples:

Critical risk review: 30 minutes  
Routine specialist review: 2 business days  
Patient follow-up: 7 days

Timer worker:

Due SLA  
↓  
Evaluate status  
↓  
if breached  
↓  
case.sla.breached  
↓  
Escalation Engine

# 19\. Escalation Engine

Escalations should be deterministic.

Example rule:

id: critical-risk-review  
<br/>when:  
case.risk_level: CRITICAL  
<br/>require:  
review_type: CLINICAL  
<br/>sla:  
duration: PT30M  
<br/>escalate:  
to_role: attending_physician  
<br/>prohibit:  
\- autonomous_case_closure

# 20\. Policy Architecture

Enterprise Case Management requires a distinct policy layer.

Four policy categories are recommended:

Access Policies  
Clinical / Domain Policies  
Operational Policies  
AI Policies

### Access policies

Answer:

Who may see or modify this?

### Domain policies

Answer:

What must happen given this situation?

### Operational policies

Answer:

How quickly must something happen?  
Who owns it?  
When does escalation occur?

### AI policies

Answer:

Can AI perform this function?  
Which model?  
Does it require human review?

# 21\. Policy Evaluation Model

Policy evaluation should produce structured outputs:

{  
"policy_id": "critical-risk-review",  
"version": "2.1",  
"decision": "REQUIRE_REVIEW",  
"reason_codes": \[  
"RISK_CRITICAL",  
"CLINICAL_ACTION"  
\],  
"required_actions": \[  
"CREATE_REVIEW"  
\],  
"prohibited_actions": \[  
"AUTO_CLOSE"  
\]  
}

Not prose.

# 22\. Case Playbooks

Introduce:

case-playbooks/

Example:

case-playbooks/  
complex-diabetes/  
CASE.md  
<br/>chronic-kidney-disease/  
CASE.md  
<br/>discharge-planning/  
CASE.md  
<br/>oncology-care/  
CASE.md

Example artifact:

\---  
id: complex-diabetes-management  
version: 1.0  
<br/>objectives:  
\- stabilize-glycemic-control  
\- reduce-complication-risk  
\- improve-medication-adherence  
<br/>initial_skills:  
\- diabetes-risk-analysis  
\- medication-review  
\- renal-risk-monitoring  
<br/>candidate_specialists:  
\- endocrinology  
\- nephrology  
\- cardiology  
\- nutrition  
<br/>recommended_milestones:  
\- baseline-assessment-complete  
\- care-plan-reviewed  
\- followup-complete  
<br/>closure_conditions:  
\- critical-risks-resolved  
\- required-reviews-complete  
\- clinician-approval  
\---

The artifact specifies intent and knowledge.

It does not encode an execution graph.

# 23\. Skill Enhancements

Existing Skills remain reusable analysis capabilities.

A Case-aware SKILL.md may add metadata:

\---  
name: renal-risk-monitoring  
version: 1.3  
type: case_skill  
<br/>applies_when:  
\- condition: diabetes  
\- risk: kidney-disease  
<br/>required_evidence:  
\- creatinine  
\- egfr  
\- medication_history  
<br/>supports_goals:  
\- renal-protection  
<br/>recommended_specialists:  
\- nephrology  
<br/>human_review:  
required_for:  
\- treatment_recommendation  
\---

The body remains SME-readable Markdown.

# 24\. Specialists

Specialists remain professional perspectives.

Examples:

specialists/  
cardiology.md  
endocrinology.md  
nephrology.md  
oncology.md  
social-work.md  
case-management.md

Each specialist should answer:

**Given my expertise, what aspects of this case require attention?**

They should not control case execution.

# 25\. Case Coordinator

Introduce an orchestration role:

Case Coordinator

The Case Coordinator is not a clinical specialist.

Responsibilities:

What changed?  
Which goals are affected?  
Which skills apply?  
Which specialists are appropriate?  
Which evidence is missing?  
Which recommendations conflict?  
Which policies apply?  
Which tasks should be proposed?  
Does human review apply?

The coordinator synthesizes.

It does not autonomously make regulated clinical decisions.

# 26\. Commands

Suggested commands:

/case create  
/case show  
/case assess  
/case plan  
/case tasks  
/case events  
/case goals  
/case evidence  
/case recommend  
/case consult  
/case review  
/case escalate  
/case summarize  
/case close

The same capabilities can be exposed through REST and MCP.

# 27\. One Orchestration Path

The enterprise architecture explicitly recommends preserving one orchestrator rather than creating different clinical brains for REST and MCP.

DCM follows:

REST  
MCP  
CLI  
UI  
Agents  
│  
└──────────────┐  
▼  
Enterprise Orchestrator  
│  
Case Runtime Adapter  
│  
Case Intelligence Engine

All entry points execute the same policies.

# 28\. Data Architecture

Introduce PostgreSQL schema:

case_management

Suggested tables:

cases  
case_subjects  
case_participants  
<br/>case_goals  
case_problems  
case_risks  
<br/>case_tasks  
case_task_dependencies  
case_assignments  
<br/>case_plans  
case_plan_versions  
case_plan_actions  
<br/>case_events  
case_evidence  
<br/>case_assessments  
case_recommendations  
case_decisions  
<br/>case_milestones  
case_reviews  
case_escalations  
<br/>case_sla_definitions  
case_sla_instances  
<br/>case_skill_runs  
case_specialist_reviews  
case_policy_evaluations  
<br/>case_notes  
case_links

# 29\. Tenant Isolation

The existing architecture requires PostgreSQL RLS for every tenant-scoped table.

Therefore every DCM table containing tenant data must implement:

ALTER TABLE case_management.cases ENABLE ROW LEVEL SECURITY;  
<br/>CREATE POLICY tenant_isolation  
ON case_management.cases  
USING (  
tenant_id =  
current_setting('app.tenant_id')::uuid  
)  
WITH CHECK (  
tenant_id =  
current_setting('app.tenant_id')::uuid  
);

Application roles must not bypass RLS.

# 30\. CaseDataService

Introduce:

CaseDataService

Architecture:

Command / MCP / UI / Case Intelligence  
│  
▼  
CaseDataService  
│  
┌───────┼────────┐  
│ │ │  
Case Event Task  
│ │ │  
└───────┼────────┘  
▼  
PostgreSQL  
│  
Audit + Outbox

Responsibilities:

- tenant context,
- RLS-safe access,
- transactions,
- optimistic locking,
- event writes,
- outbox writes,
- audit calls,
- artifact references.

No higher-level service should directly mutate case tables.

# 31\. Optimistic Concurrency

Case management is inherently collaborative.

All primary aggregates should include:

version  
updated_at  
updated_by

Example:

UPDATE case_management.cases  
SET  
status = :status,  
version = version + 1  
WHERE  
case_id = :case_id  
AND  
version = :expected_version;

Zero rows updated results in:

409 Conflict

The caller reloads and reconciles.

# 32\. FHIR Alignment

SynapseMD's enterprise architecture treats PostgreSQL as the system of record and FHIR as an interoperability projection.

DCM should maintain the same approach.

Relevant FHIR mappings:

| DCM Concept       | FHIR Resource  |
| ----------------- | -------------- |
| Case Subject      | Patient        |
| Problem           | Condition      |
| Clinical evidence | Observation    |
| Goal              | Goal           |
| Care Plan         | CarePlan       |
| Clinical Task     | Task           |
| Team              | CareTeam       |
| Referral          | ServiceRequest |
| Encounter         | Encounter      |

However, FHIR does not become the case execution engine.

Internal DCM concepts remain native:

case_plan_version  
policy_evaluation  
skill_run  
specialist_review  
case_recommendation  
case_decision  
case_escalation  
case_event

# 33\. Clinical Data vs Case Data

Maintain strict separation:

clinical.\*

represents clinical truth.

case_management.\*

represents management and coordination.

Example:

clinical.observations  
│  
▼  
HealthDataService  
│  
▼  
Case Intelligence  
│  
▼  
case_management.case_assessments  
case_management.case_recommendations

This boundary is important for data governance and semantic correctness.

# 34\. Authentication and Authorization

DCM reuses existing:

OIDC  
MFA  
JWT  
RBAC  
ABAC  
Purpose of Use  
Consent  
Break Glass

The enterprise architecture already requires centralized RBAC + ABAC rather than route-level if role == ... logic.

DCM authorization should evaluate:

Actor  
Role  
Tenant  
Case  
Relationship  
Purpose  
Consent  
Data class  
Assignment  
Action  
Case state

Example:

Can Social Worker X read this case?  
<br/>Tenant ✓  
Assignment ✓  
Purpose treatment  
Data class PHI  
Consent ✓  
Resource assigned case  
Decision ALLOW

# 35\. Human Review

Human review becomes a real domain entity.

Suggested fields:

review_id  
case_id  
review_type  
source  
reason  
risk_level  
status  
requested_by  
assigned_to  
reviewer_role  
due_at  
decision  
decision_reason  
approved_at

Review types:

AI_RECOMMENDATION  
CLINICAL_ESCALATION  
HIGH_RISK_ACTION  
CASE_CLOSURE  
POLICY_EXCEPTION  
BREAK_GLASS  
SPECIALIST_REVIEW

# 36\. LLM Architecture

DCM must never call external LLM providers directly.

It must use the existing enterprise PHI-safe pipeline:

Purpose / Consent  
↓  
Minimal Context Selection  
↓  
PHI Anonymization  
↓  
Model Policy Engine  
↓  
LLM  
↓  
Guardrails  
↓  
Authorized Deanonymization  
↓  
Audit Hashes

The enterprise architecture explicitly mandates this pipeline and forbids raw PHI exposure to external models.

# 37\. Context Minimization

Do not send an entire case to the LLM.

The Case Intelligence Engine should build:

Minimal Case Context

based on:

Operation  
Skill  
Specialist  
Purpose  
Risk  
Relevant Evidence  
Applicable Policy

Example:

Cardiology specialist

should receive cardiology-relevant evidence rather than the entire longitudinal health record.

# 38\. Model Routing

Extend the existing model policy function:

route(  
command,  
data_class,  
tenant_policy,  
catalog  
)

into:

route_case_operation(  
operation,  
case_type,  
task_type,  
risk_level,  
data_class,  
tenant_policy,  
required_capabilities  
)

Example:

CASE_SUMMARY  
→ healthcare standard tier  
<br/>NEXT_ACTION_RECOMMENDATION  
→ healthcare safety tier  
<br/>SPECIALIST_REVIEW  
→ critical tier  
<br/>CASE_POLICY_EVALUATION  
→ deterministic; no LLM  
<br/>SLA_CHECK  
→ deterministic; no LLM

The existing model architecture already requires policy controls for BAA, residency, cost, safety tier, and tenant restrictions.

# 39\. Artifact Registry

Add enterprise runtime catalog:

artifact_registry

Fields:

artifact_id  
artifact_type  
name  
version  
content_hash  
status  
owner  
approved_by  
effective_from  
effective_to  
risk_class  
tenant_scope  
source_commit

Artifact types:

COMMAND  
SKILL  
SPECIALIST  
POLICY  
CASE_PLAYBOOK

The filesystem/Git repository remains source-controlled authoring.

The registry becomes production runtime authority.

# 40\. Artifact Governance

Production deployment should support:

DRAFT  
REVIEW  
APPROVED  
ACTIVE  
RETIRED

High-risk artifacts may require:

Clinical approval  
Security approval  
Compliance approval

Cases must remember the exact artifact version used.

# 41\. Decision Reproducibility

Every material recommendation should capture:

case version  
playbook version  
policy versions  
skill versions  
specialist versions  
model id  
model policy decision  
evidence references  
deterministic calculations  
prompt template version  
human reviewer

This allows SynapseMD to answer:

**Why did the system recommend this action at that time?**

# 42\. Audit Architecture

The existing enterprise design distinguishes operational logging from compliance auditing and requires append-only, hash-chained audit storage.

DCM should audit:

case.created  
case.updated  
case.viewed  
case.assigned  
<br/>goal.created  
goal.changed  
<br/>task.created  
task.assigned  
task.completed  
<br/>recommendation.generated  
recommendation.approved  
recommendation.rejected  
<br/>policy.evaluated  
policy.override.requested  
<br/>specialist.invoked  
<br/>review.created  
review.completed  
<br/>case.escalated  
case.closed  
case.reopened  
<br/>artifact.version.used

# 43\. Logging Architecture

Operational logs must remain PHI-free.

Allowed:

tenant UUID  
case UUID  
trace ID  
operation name  
latency  
policy decision  
model ID  
status  
error type

Do not log:

Patient name  
MRN  
Lab values  
Clinical note  
Prompt body  
LLM completion

This follows the enterprise logging requirements already established for SynapseMD.

# 44\. OpenTelemetry

All operations should be traceable.

Example:

POST /cases/{id}/evaluate  
│  
▼  
CaseService  
│  
CaseDataService  
│  
CaseIntelligenceEngine  
┌────┼────────┐  
▼ ▼ ▼  
GoalEngine Policy SkillRouter  
│  
Module 21  
│  
SpecialistRouter  
│  
RecommendationEngine  
│  
ReviewService

Recommended span attributes:

tenant_id  
case_id  
case_type  
operation  
artifact_id  
artifact_version  
skill_id  
specialist_id  
policy_id  
model_id  
risk_class

No PHI.

# 45\. MCP Interfaces

Recommended MCP tools:

create_case  
get_case  
search_cases  
<br/>assess_case  
<br/>get_case_goals  
add_case_goal  
update_case_goal  
<br/>get_case_tasks  
create_case_task  
complete_case_task  
<br/>add_case_event  
get_case_events  
<br/>get_case_evidence  
<br/>recommend_case_actions  
<br/>consult_case_specialist  
<br/>get_case_plan  
propose_case_plan  
<br/>request_case_review  
complete_case_review  
<br/>escalate_case  
close_case  
reopen_case

MCP exposes business capabilities.

It must not expose internal state mutations such as:

set_database_state  
bypass_policy  
skip_review  
execute_sql

# 46\. REST API

Illustrative endpoints:

POST /api/v1/cases  
GET /api/v1/cases/{id}  
GET /api/v1/cases  
<br/>POST /api/v1/cases/{id}/evaluate  
<br/>GET /api/v1/cases/{id}/goals  
POST /api/v1/cases/{id}/goals  
<br/>GET /api/v1/cases/{id}/tasks  
POST /api/v1/cases/{id}/tasks  
<br/>POST /api/v1/cases/{id}/events  
<br/>GET /api/v1/cases/{id}/plan  
POST /api/v1/cases/{id}/plan/propose  
<br/>POST /api/v1/cases/{id}/consult  
<br/>POST /api/v1/cases/{id}/reviews  
<br/>POST /api/v1/cases/{id}/escalate  
<br/>POST /api/v1/cases/{id}/close

# 47\. Internal Python Structure

Recommended structure:

synapsemd/  
│  
├── case_management/  
│ │  
│ ├── domain/  
│ │ ├── case.py  
│ │ ├── goal.py  
│ │ ├── task.py  
│ │ ├── event.py  
│ │ ├── evidence.py  
│ │ ├── plan.py  
│ │ ├── milestone.py  
│ │ ├── recommendation.py  
│ │ ├── decision.py  
│ │ └── review.py  
│ │  
│ ├── services/  
│ │ ├── case_service.py  
│ │ ├── case_data_service.py  
│ │ ├── task_service.py  
│ │ └── review_service.py  
│ │  
│ ├── intelligence/  
│ │ ├── case_intelligence_engine.py  
│ │ ├── coordinator.py  
│ │ ├── recommendation_engine.py  
│ │ └── context_builder.py  
│ │  
│ ├── engines/  
│ │ ├── goal_engine.py  
│ │ ├── policy_engine.py  
│ │ ├── milestone_engine.py  
│ │ ├── escalation_engine.py  
│ │ ├── sla_engine.py  
│ │ └── assignment_engine.py  
│ │  
│ ├── routing/  
│ │ ├── skill_router.py  
│ │ ├── specialist_router.py  
│ │ └── artifact_router.py  
│ │  
│ ├── repository/  
│ │ ├── case_repository.py  
│ │ ├── event_repository.py  
│ │ └── outbox_repository.py  
│ │  
│ └── workers/  
│ ├── event_worker.py  
│ ├── sla_worker.py  
│ └── outbox_worker.py  
│  
├── commands/  
├── skills/  
├── specialists/  
├── policies/  
└── case-playbooks/

# 48\. Case Evaluation Sequence

Case Event  
│  
▼  
Authenticate  
│  
▼  
Authorize / Purpose / Consent  
│  
▼  
Load Case State  
│  
▼  
Load Relevant Clinical Context  
│  
▼  
Evaluate Deterministic Policies  
│  
▼  
Evaluate Goals / Milestones / SLA  
│  
▼  
Identify Relevant Skills  
│  
▼  
Run Deterministic Skills / Module 21  
│  
▼  
Identify Relevant Specialists  
│  
▼  
Build Minimal Context  
│  
▼  
Optional PHI-safe LLM Processing  
│  
▼  
Generate Candidate Recommendations  
│  
▼  
Policy / Guardrail Validation  
│  
▼  
Create Human Review if Required  
│  
▼  
Update Case Plan  
│  
▼  
Persist Case Event + Audit + Outbox

# 49\. Example: Complex Diabetes Case

New event:

HbA1c increases from 7.4 to 9.2

Processing:

LAB RECEIVED  
│  
▼  
Case Event  
│  
▼  
Current Case  
├── Diabetes  
├── CKD  
├── Hypertension  
└── Poor medication adherence  
│  
▼  
Goal Engine  
├── glycemic-control → AT_RISK  
└── renal-protection → ACTIVE  
│  
▼  
Policy Engine  
└── evaluate escalation requirements  
│  
▼  
Skill Router  
├── diabetes-trend-analysis  
├── medication-adherence  
├── renal-risk-analysis  
└── nutrition-analysis  
│  
▼  
Module 21  
├── deterministic risk scoring  
└── trend calculations  
│  
▼  
Specialist Router  
├── endocrinology  
├── nephrology  
└── nutrition  
│  
▼  
Case Coordinator  
│  
▼  
Candidate Actions  
├── Review medication adherence  
├── Review CGM trend  
├── Endocrinology review  
├── Renal monitoring  
└── Nutrition consultation  
│  
▼  
Human Review / Approval

No BPMN process definition is required.

# 50\. Privacy and PHI

Case management adds substantial PHI risk because case context often aggregates data across multiple clinical sources.

Therefore:

1. Context minimization is mandatory.
2. Raw case state should not be passed to LLMs.
3. External LLM access must pass purpose + consent checks.
4. Anonymization failure must fail closed.
5. Re-identification remains an audited action.
6. LLM prompts and completions are stored as hashes, not raw PHI.

These requirements align directly with the enterprise PHI architecture.

# 51\. Security Controls

DCM inherits:

TLS 1.2+  
mTLS  
Vault / KMS  
per-tenant keys  
private networking  
network egress controls  
RLS  
short-lived JWT  
OIDC  
MFA  
signed containers  
SBOM  
backup / PITR  
threat detection

from the enterprise architecture.

Additional DCM threats include:

- unauthorized case assignment,
- malicious case reassignment,
- fabricated events,
- recommendation injection,
- artifact tampering,
- policy bypass,
- stale artifact versions,
- duplicate event processing,
- unauthorized closure,
- malicious prompt content inside case notes.

# 52\. Idempotency

Event-driven systems must assume duplicate delivery.

All commands that may be retried should accept:

idempotency_key

Example:

POST /cases/{id}/events  
Idempotency-Key: 3ae...

Uniqueness should be tenant-scoped.

Repeated submission returns original result rather than creating duplicate tasks or events.

# 53\. Failure Handling

Failures should be categorized:

TRANSIENT  
PERMANENT  
POLICY_DENIED  
AUTHORIZATION_DENIED  
DATA_INVALID  
DEPENDENCY_UNAVAILABLE  
HUMAN_REVIEW_REQUIRED

Retries are appropriate only for transient failures.

LLM failure must not leave case state partially changed.

# 54\. AI Failure Strategy

If AI is unavailable:

Case state remains valid.  
Policies continue running.  
Tasks continue operating.  
SLA continues operating.  
Module 21 continues operating.

Only AI-assisted capabilities degrade.

This is an important enterprise principle:

**The Case Management platform must remain operational without an LLM.**

# 55\. Human Override

Human actors may override certain recommendations.

Override should require:

Actor  
Reason  
Original recommendation  
New decision  
Policy context  
Timestamp

Some policies must remain non-overridable except through formal break-glass or administrative procedures.

# 56\. Case Closure

Closure is a policy decision, not simply a user operation.

Possible closure conditions:

mandatory goals completed  
required tasks completed  
open critical risks resolved  
mandatory reviews completed  
required evidence present  
closure approval obtained

An LLM must never independently close a regulated case.

# 57\. Reopening

Cases may reopen when:

new evidence arrives  
risk recurs  
follow-up fails  
policy requires  
human initiates

Reopen should preserve previous closure state and create a new event:

case.reopened

not rewrite history.

# 58\. Case Linking

Support relationships:

parent case  
child case  
related case  
duplicate case  
merged case  
follow-up case

Useful for:

Episode management  
Multiple complications  
Family cases  
Cross-organizational coordination

# 59\. Control Plane

Case Management control-plane configuration should include:

case type definitions  
active playbook versions  
policy versions  
SLA definitions  
escalation matrices  
assignment rules  
review requirements  
artifact versions  
allowed models  
retention  
case permissions

Configuration can be tenant-specific.

# 60\. Enterprise Artifact Promotion

Suggested promotion lifecycle:

Git  
↓  
Validation  
↓  
Security / Clinical Review  
↓  
Artifact Registry  
↓  
Staging  
↓  
Evaluation Tests  
↓  
Approval  
↓  
Production Activation

The artifact content remains Markdown.

Enterprise governance wraps around it.

# 61\. Testing Strategy

## Unit tests

Cover:

State transitions  
Goal evaluation  
Policy decisions  
SLA calculations  
Artifact parsing  
Concurrency  
Idempotency  
Assignment rules

## Integration tests

Cover:

Postgres RLS  
Audit  
Outbox  
HealthDataService  
Model policy  
Review queue  
FHIR mapping

## Security tests

Cover:

Cross-tenant access  
PHI in logs  
Unauthorized case closure  
Policy bypass  
Prompt injection  
Artifact tampering  
Break-glass abuse

## AI evaluation

Measure:

Recommendation relevance  
Unsupported recommendation rate  
Specialist-routing accuracy  
Evidence citation accuracy  
Policy violation rate  
Hallucination rate  
Human rejection rate

# 62\. Observability Metrics

Recommended DCM metrics:

cases_open  
cases_created  
cases_closed  
<br/>case_age  
<br/>goals_at_risk  
<br/>tasks_overdue  
<br/>sla_breaches  
<br/>case_escalations  
<br/>recommendations_generated  
<br/>recommendations_approved  
recommendations_rejected  
<br/>human_review_age  
<br/>policy_denials  
<br/>artifact_failures  
<br/>skill_failures  
<br/>specialist_invocations  
<br/>llm_fallback_rate

# 63\. Enterprise Deployment

DCM should use the existing deployment topology, not create a separate stack.

Potential workloads:

platform-api  
mcp-server  
<br/>case-worker  
sla-worker  
outbox-worker  
<br/>specialist-worker  
review-worker

Infrastructure remains:

Kubernetes  
PostgreSQL  
Object Store  
Vault/KMS  
OTel Collector  
SIEM  
OIDC IdP  
LLM Providers

The existing architecture already defines production deployment around HA PostgreSQL, Vault, OTel, NetworkPolicies, and Kubernetes.

# 64\. Personal / Local Mode

The SynapseMD philosophy of starting small should continue.

Personal mode may use:

Local JSON  
+  
Markdown case playbook  
+  
Commands  
+  
Skills  
+  
Specialists

Enterprise mode switches adapters:

Postgres  
RLS  
OIDC  
Audit  
Policies  
CaseDataService  
Distributed workers

The concepts and commands remain the same.

# 65\. Cross-Domain Extensibility

The case runtime remains domain-neutral.

### Healthcare

Case Patient case  
Skill Medication reconciliation  
Specialist Cardiologist  
Policy Clinical escalation

### Insurance

Case Claim  
Skill Fraud analysis  
Specialist Claims investigator  
Policy Coverage policy

### Legal

Case Legal matter  
Skill Contract analysis  
Specialist Counsel  
Policy Legal compliance

### Government

Case Citizen application  
Skill Eligibility analysis  
Specialist Department officer  
Policy Government regulation

The runtime does not change.

# 66\. What We Explicitly Will Not Build

The first architecture should avoid:

BPMN  
Full workflow designer  
General-purpose orchestration DSL  
LLM-generated unrestricted workflows  
Autonomous clinical execution  
Hard-coded disease workflows  
Separate case database technology  
Separate identity stack  
Separate AI gateway  
Separate audit subsystem

These would dilute the architecture.

# 67\. Recommended Delivery Phases

## Phase A — Case Foundation

Build:

Case aggregate  
Goals  
Tasks  
Events  
Evidence  
Postgres schema  
CaseDataService  
RLS  
Audit  
Optimistic locking

No AI required.

## Phase B — Deterministic Case Intelligence

Add:

Goal Engine  
Milestone Engine  
Policy Engine  
SLA Engine  
Escalation Engine  
Assignment Engine  
Case Plan versions

## Phase C — Artifact Runtime

Add:

Case Playbooks  
Policy artifacts  
Artifact Registry  
Skill routing  
Specialist routing  
Version pinning

## Phase D — AI-Assisted Case Intelligence

Add:

Case Coordinator  
Recommendation Engine  
Context Builder  
PHI-safe LLM route  
Multidisciplinary synthesis  
Human review

## Phase E — Distributed Enterprise Runtime

Add:

Transactional outbox  
Kafka  
Worker pool  
Specialist workers  
Notification integration  
Scale testing  
HA

## Phase F — Advanced Intelligence

Possible later capabilities:

Case similarity  
Outcome prediction  
Next-best-action ranking  
Care pathway optimization  
Cross-case population intelligence  
Learning from human decisions  
Adaptive playbook recommendations

All subject to privacy and clinical-governance controls.

# 68\. Definition of Enterprise-Grade DCM

SynapseMD Dynamic Case Management can be considered enterprise-grade when the platform can demonstrate:

1. Every case is tenant-isolated through PostgreSQL RLS.
2. Multiple users can collaborate without silent overwrite through optimistic concurrency.
3. Every material case change generates immutable event and audit records.
4. Case history can reconstruct why a recommendation or decision occurred.
5. Playbook, skill, specialist, and policy versions are traceable.
6. LLM invocation cannot proceed if PHI anonymization, consent, BAA, or residency policy fails.
7. Case processing continues when external LLMs are unavailable.
8. Critical policies and SLA escalations are deterministic.
9. Human review is mandatory for configured high-risk actions.
10. SMEs can introduce new case types without modifying the Case Engine.
11. The same case-management runtime works through CLI, REST, MCP, and enterprise UI.
12. Operational logs contain no PHI.
13. Audit events are durable and tamper-evident.
14. FHIR interoperability does not dictate internal orchestration design.
15. A case can dynamically change its plan in response to new evidence without a predefined process graph.

# 69\. Architectural Decision Summary

| Decision                 | Recommendation                                |
| ------------------------ | --------------------------------------------- |
| Workflow paradigm        | Goal/Event-driven Dynamic Case Management     |
| BPMN                     | Do not use                                    |
| Case SoR                 | PostgreSQL                                    |
| Clinical SoR             | Existing SynapseMD PostgreSQL clinical model  |
| Case/Clinical separation | Separate schemas                              |
| FHIR                     | Projection / interoperability                 |
| Event architecture       | Postgres event journal + transactional outbox |
| Messaging V1             | Internal worker                               |
| Messaging scale          | Kafka                                         |
| Concurrency              | Optimistic locking                            |
| Domain knowledge         | Markdown artifacts                            |
| Case definition          | CASE.md playbooks                             |
| Rules/policies           | Versioned policy artifacts                    |
| AI                       | Assistive, not authoritative                  |
| Deterministic controls   | Mandatory                                     |
| Human review             | First-class entity                            |
| Audit                    | Append-only, signed/hash-chained              |
| Tenant security          | PostgreSQL RLS                                |
| AI privacy               | Existing PHI-safe model pipeline              |
| Observability            | OpenTelemetry                                 |
| Runtime                  | Domain-neutral                                |
| Extensibility            | Skills + Specialists + Policies + Playbooks   |

#

# 70\. Final Reference Architecture

USER / SYSTEM / EVENT  
│  
▼  
API GATEWAY / MCP  
│  
▼  
ENTERPRISE ORCHESTRATOR  
│  
┌────────────┴────────────┐  
│ │  
▼ ▼  
Command Runtime Case Runtime  
│  
┌───────────────┼───────────────┐  
▼ ▼ ▼  
Goal Engine Policy Engine Event Engine  
│ │ │  
▼ ▼ ▼  
Milestone Engine SLA/Escalation Task Engine  
│ │ │  
└───────────────┼───────────────┘  
▼  
Case Intelligence Engine  
│  
┌────────────────────────────┼──────────────────────────┐  
▼ ▼ ▼  
Skills Specialists Module 21  
│ │ │  
└────────────────────────────┼──────────────────────────┘  
▼  
Evidence  
│  
▼  
Recommendation Engine  
│  
AI where permitted  
│  
▼  
Guardrails  
│  
▼  
Human Review  
│  
▼  
Case Decision  
│  
▼  
Case Plan  
│  
▼  
Case Actions  
│  
┌───────────────────────────┼────────────────────────┐  
▼ ▼ ▼  
HealthDataService CaseDataService External APIs  
│ │  
└──────────────┬────────────┘  
▼  
PostgreSQL  
SoR + RLS + Outbox  
│  
┌───────────────┼────────────────┐  
▼ ▼ ▼  
FHIR Projection Audit/WORM Event Bus  
<br/><br/>DOMAIN INTELLIGENCE  
────────────────────────────────────────────────────────  
<br/>commands/  
skills/  
specialists/  
policies/  
case-playbooks/  
<br/><br/>ENTERPRISE TRUST LAYER  
────────────────────────────────────────────────────────  
<br/>OIDC + MFA  
RBAC + ABAC  
Consent  
RLS  
Vault / KMS  
PHI Anonymization  
Model Policy  
Guardrails  
Audit  
OpenTelemetry  
SIEM

# 71\. Core Architectural Statement

The architecture should formally adopt the following definition:

**SynapseMD Dynamic Case Management is not a workflow engine. It is an enterprise-grade, goal-driven, event-driven orchestration capability in which the platform manages trusted execution and case state while domain experts define case knowledge through versioned artifacts.**

And:

**The Case Engine remains domain-agnostic. Healthcare expertise belongs in Case Playbooks, Skills, Specialists, Policies, and deterministic clinical modules—not in the technical runtime.**

The resulting SynapseMD architecture becomes:

Commands  
+  
Skills  
+  
Specialists  
+  
Policies  
+  
Case Playbooks  
+  
Dynamic Case Intelligence  
+  
Deterministic Analytics  
+  
Governed AI  
+  
Enterprise Trust Platform

This preserves the central idea behind SynapseMD:

**Sophisticated enterprise AI does not require beginning with a massive framework. Start with small, stable architectural primitives; keep domain knowledge independent; introduce enterprise trust and scale as adoption grows.**