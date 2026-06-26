# SynapseMD Enterprise Implementation Plan

This document translates the [Enterprise Architecture Blueprint](../docs/enterprise-architecture.md) into a phased implementation plan with concrete tasks, tests, and documentation deliverables.

## Overview

The current SynapseMD system is a single-user, file-based CLI tool. This plan defines how to transform it into a **multi-tenant, regulatory-compliant, AI-powered health platform** suitable for healthcare organizations, insurance providers, and digital health companies.

### Key Transformation Axes

| Dimension | Current State | Target State |
|---|---|---|
| Users | 1 (local filesystem) | 100k+ (multi-tenant SaaS) |
| Storage | JSON files on disk | Encrypted cloud databases |
| LLM | Claude Code CLI | Health-specialized LLM fleet + RAG |
| Compliance | None | HIPAA, GDPR, SOC 2 Type II, HL7 FHIR |
| AI Governance | None | Full explainability, audit trail, human-in-the-loop |
| PHI Handling | Stored in plaintext | De-identified, tokenized, encrypted |
| Deployment | `git clone` local | Kubernetes / managed cloud |

### Recommended Delivery Order

Start with a narrow vertical slice:

**Authenticated tenant-scoped API → PHI anonymization → mocked LLM call → audit event**

Once that path is safe, expand horizontally into FHIR migration, RAG, governance, and compliance certification.

> **Note on reasoning traces:** Avoid storing raw chain-of-thought. Instead store structured reasoning summaries, citations, assumptions, confidence, safety checks, and model metadata. This provides auditability without retaining sensitive or provider-restricted hidden reasoning.

---

## Phase 0: Project Foundation

**Goal:** Establish repository structure, tooling, and architectural decisions before feature work.

### Implementation Tasks

- [ ] Define target backend structure: FastAPI services for `api-gateway`, `command-service`, `skill-service`, `anonymization-service`, `rag-service`, and `audit-service`
- [ ] Add `pyproject.toml`, formatting, linting, type checking, Dockerfiles, `.env.example`, and CI workflows
- [ ] Create architecture decision records (ADRs) for:
  - Cloud provider choice
  - Identity provider (Auth0 / Cognito / Keycloak)
  - FHIR backend (HAPI FHIR / HealthLake / Azure Health Data Services)
  - Vector DB (Weaviate / Pinecone)
  - Secrets vault (HashiCorp Vault)
  - LLM providers and BAAs

### Tests

- [ ] CI smoke test pipeline (build + lint + typecheck)
- [ ] Docker build test for each service skeleton
- [ ] Dependency audit in CI (`pip-audit`)

### Documentation

- [ ] `docs/implementation-roadmap.md` — high-level timeline and milestones
- [ ] `docs/local-development.md` — setup, env vars, running services locally
- [ ] `docs/adr/` — initial ADRs for key technology choices

---

## Phase 1: Auth, RBAC, and Multi-Tenancy

**Goal:** Secure API layer with tenant isolation before any PHI or AI work.

**Timeline:** Weeks 1–4 (per architecture doc Phase 1)

### Implementation Tasks

- [ ] Deploy API Gateway (Kong / AWS API GW) or FastAPI gateway service
- [ ] Integrate identity provider (Auth0 / Cognito / Keycloak)
- [ ] Implement JWT validation + RBAC middleware
- [ ] Create `tenants` and `users` tables (see architecture schema)
- [ ] Enforce `{tenant_id, user_id}` on all request contexts
- [ ] Implement PostgreSQL row-level security policies:
  ```sql
  CREATE POLICY user_isolation ON health_records
    USING (user_id = current_setting('app.user_id')::uuid
           AND tenant_id = current_setting('app.tenant_id')::uuid);
  ```
- [ ] Wrap existing commands in REST endpoints (thin adapter layer)
- [ ] Support both tenancy models:
  - **Model A:** Org-scoped (hospitals, clinics, insurers)
  - **Model B:** Consumer SaaS (individual users with family sub-accounts)
- [ ] Keep existing command `.md` files unchanged during adapter phase

### Tests

- [ ] Unit tests for JWT claim parsing and RBAC decision matrix
- [ ] Integration tests proving tenant A cannot read tenant B data
- [ ] PostgreSQL RLS tests with malicious tenant/user ID injection
- [ ] API tests for unauthenticated, unauthorized, and valid request flows
- [ ] Role-based endpoint access tests (`patient`, `clinician`, `admin`, `auditor`)

### Documentation

- [ ] `docs/auth-rbac.md` — roles, scopes, JWT claims
- [ ] `docs/multi-tenancy.md` — tenancy models, isolation levels
- [ ] OpenAPI spec with tenant-scoped endpoint examples

---

## Phase 2: PHI Safety and Anonymization Pipeline

**Goal:** Ensure PHI never reaches the LLM in raw form. Fail closed on any anonymization failure.

**Timeline:** Weeks 5–8 (per architecture doc Phase 2)

### Implementation Tasks

- [ ] Deploy Microsoft Presidio anonymization service
- [ ] Implement PHI detection (NER-based): names, DOB, addresses, MRNs, phone numbers, emails, SSN
- [ ] Implement tokenization: replace PHI with stable tokens (`{TOKEN:patient:a3f2}`)
- [ ] Deploy HashiCorp Vault for token ↔ real value mapping
- [ ] Implement generalization: dates → age ranges, ZIP → region codes
- [ ] Add validation pass: re-run NER on output, assert zero PHI remains
- [ ] Intercept all LLM calls: anonymize before → de-anonymize after for authorized users
- [ ] Add log redaction middleware (PHI never in logs — only tokens and hashes)
- [ ] Enforce PHI handling rules by data path:
  - User → API: PHI allowed (TLS, authenticated)
  - API → LLM: PHI NEVER sent
  - API → Database: PHI encrypted at rest (tenant KMS key)
  - API → Logs: PHI NEVER
  - Audit logs: token references only, immutable append-only

### Tests

- [ ] PHI fixture corpus: names, DOBs, MRNs, emails, phones, addresses, dates, free-text clinical notes
- [ ] Regression tests asserting raw PHI never reaches mocked LLM provider payloads
- [ ] Log-scan tests that fail CI if PHI-like values appear in structured logs
- [ ] Failure-mode tests: Vault unavailable, Presidio unavailable, partial anonymization detected
- [ ] Staging validation: zero PHI reaches LLM in end-to-end test suite

### Documentation

- [ ] `docs/phi-handling.md` — rules by data path, HIPAA Safe Harbor mapping
- [ ] `docs/anonymization-pipeline.md` — pipeline steps, Presidio integration
- [ ] Incident runbook for PHI leak detection and response

---

## Phase 3: File-to-FHIR Data Migration

**Goal:** Replace flat JSON tracker files with HL7 FHIR R4 resources for interoperability and compliance.

**Timeline:** Weeks 9–16 (per architecture doc Phase 3)

### Implementation Tasks

- [ ] Introduce `DataAccessLayer` abstraction so commands read/write through an interface
- [ ] Deploy HAPI FHIR Server (local dev) or Amazon HealthLake / Azure Health Data Services (cloud)
- [ ] Implement FHIR resource mappings:

  | Current JSON File | FHIR Resource |
  |---|---|
  | `profile.json` | `Patient` |
  | `allergies.json` | `AllergyIntolerance` |
  | `medications/*.json` | `MedicationRequest` + `MedicationAdministration` |
  | `*-tracker.json` | `Observation` (with LOINC codes) |
  | `fitness-logs/` | `Observation` (LOINC 55423-8, 41950-7) |
  | `radiation-records.json` | `ImagingStudy` + `Observation` |
  | `surgery-records/` | `Procedure` |
  | `discharge-summaries/` | `Composition` (LOINC 18842-5) |
  | `interactions/` | `ClinicalUseDefinition` |

- [ ] Build idempotent migration scripts: JSON trackers → FHIR bundles
- [ ] Add dual-read or migration validation mode before full FHIR switch
- [ ] Update commands to use DataAccessLayer (command `.md` logic unchanged)
- [ ] Deploy vector database (Weaviate) for RAG preparation

### Tests

- [ ] Golden-file tests for JSON-to-FHIR conversion per resource type
- [ ] FHIR validation tests against R4 schemas/profiles
- [ ] Migration idempotency tests (run twice, same result)
- [ ] Round-trip tests: legacy JSON → FHIR → normalized command output
- [ ] Performance tests for large patient histories

### Documentation

- [ ] `docs/fhir-mapping.md` — complete mapping table with LOINC/RxNorm/SNOMED codes
- [ ] `docs/data-migration-guide.md` — step-by-step migration procedure
- [ ] `docs/fhir-local-setup.md` — HAPI FHIR local development setup

---

## Phase 4: Audit and Observability

**Goal:** Immutable audit trail and full observability for compliance and operations.

### Implementation Tasks

- [ ] Define audit event schema (see architecture doc §9):
  - `event_type`, `actor`, `resource`, `ai`, `outcome`, `signature`
- [ ] Implement Kafka-compatible event producer (start with local Redpanda/Kafka)
- [ ] Stream events to immutable storage (Kafka → S3 Glacier, 7-year HIPAA retention)
- [ ] Index audit events in OpenSearch for real-time querying
- [ ] Add OpenTelemetry tracing across all services
- [ ] Add Prometheus metrics:
  - LLM token consumption by command
  - Guardrail trigger rate (% blocked)
  - Human review queue depth + SLA breach alerts
  - PHI tokenization failure rate (must be 0%)
  - Per-tenant API latency p50/p95/p99
- [ ] Add structured JSON logging with PHI redaction
- [ ] Implement data lineage tracking (record → anonymization → LLM → guardrail → delivery)

### Tests

- [ ] Audit event contract/schema validation tests
- [ ] HMAC/signature verification tests for audit events
- [ ] Trace propagation tests across API → command → anonymization → LLM
- [ ] Metrics endpoint tests (Prometheus scrape)
- [ ] Log redaction tests in observability pipeline

### Documentation

- [ ] `docs/audit-events.md` — event schema, retention policy
- [ ] `docs/observability.md` — stack, dashboards, alert thresholds
- [ ] Dashboard and alert runbooks

---

## Phase 5: LLM Router and Provider Layer

**Goal:** Route health tasks to the appropriate model based on complexity, sensitivity, and tenant policy.

**Timeline:** Weeks 17–20 (per architecture doc Phase 4, partial)

### Implementation Tasks

- [ ] Implement `HealthLLMRouter` with routing table by `(complexity, data_sensitivity)`
- [ ] Add provider adapters: Anthropic, OpenAI, Google Health AI, local OpenAI-compatible (vLLM/Ollama)
- [ ] Map commands to complexity:
  - **CRITICAL:** `consult`, `specialist`, `mental-health`, `psych-assess`
  - **COMPLEX:** `report`, `ai`, `health-trend-analyzer`, `interaction`
  - **SIMPLE:** `profile`, `query`, `get-profile`
- [ ] Add prompt hashing, response hashing, latency, token accounting
- [ ] Implement fallback behavior with safe degradation
- [ ] Add tenant-level model allowlists for regulated deployments
- [ ] Support on-premise/air-gapped deployment (Meditron-70B, custom SLM via vLLM)

### Tests

- [ ] Router decision matrix tests (all complexity × sensitivity combinations)
- [ ] Mock provider contract tests
- [ ] Fallback tests when primary provider fails
- [ ] Cost-accounting tests (token usage per command)
- [ ] Tests ensuring pseudonymized data only routes to approved providers

### Documentation

- [ ] `docs/llm-routing.md` — routing table, model selection rationale
- [ ] `docs/model-provider-setup.md` — provider configuration, BAAs
- [ ] `docs/tenant-ai-policy.md` — per-tenant model restrictions

---

## Phase 6: RAG Clinical Knowledge

**Goal:** Ground LLM responses in authoritative, current clinical knowledge.

**Timeline:** Weeks 9–16 (parallel with Phase 3)

### Implementation Tasks

- [ ] Build ingestion pipeline for:
  - Public: PubMed, FDA DailyMed, WHO ICD-11, clinical guidelines (AHA, ADA, USPSTF), CDC vaccine schedules, SNOMED/LOINC/RxNorm
  - Org-specific: hospital formulary, internal protocols, payer policies, de-identified outcomes
- [ ] Implement chunking, metadata extraction, embedding generation
- [ ] Deploy vector storage (Weaviate) with health-specific embeddings (e.g., S-PubMedBert)
- [ ] Implement hybrid retrieval: vector search + keyword/BM25 (Reciprocal Rank Fusion)
- [ ] Add cross-encoder re-ranking (top 10 → top 3)
- [ ] Add citation extraction and freshness checks (flag sources > 5–10 years old)
- [ ] Integrate RAG context injection for consultation and analysis commands
- [ ] Use MedSpaCy NER + UMLS concept normalization for query understanding

### Tests

- [ ] Ingestion tests for supported source formats
- [ ] Embedding metadata tests (evidence level, publication date, specialty)
- [ ] Retrieval quality eval set with expected documents
- [ ] Citation-required tests for clinical claims in responses
- [ ] Freshness tests for outdated clinical sources

### Documentation

- [ ] `docs/rag-architecture.md` — pipeline, retrieval strategy
- [ ] `docs/knowledge-ingestion.md` — source list, ingestion schedule
- [ ] `docs/citation-policy.md` — when citations are required

---

## Phase 7: AI Governance and Human Review

**Goal:** Medical guardrails, explainability, and human-in-the-loop for safety-sensitive decisions.

**Timeline:** Weeks 17–20 (per architecture doc Phase 4)

### Implementation Tasks

- [ ] Implement `MedicalGuardrails` validation layer:
  - **Hard blocks:** diagnosis claims, medication change recommendations, certainty claims
  - **Soft flags:** recommendations (add disclaimer), clinical claims (require citation)
- [ ] Add confidence scoring and disclaimer injection (threshold < 0.7 → human review)
- [ ] Store structured reasoning summaries (not raw CoT): data sources, assumptions, alternatives, conclusion, confidence
- [ ] Implement human review queue for:
  - `/consult`, `/specialist` (MDT)
  - Guardrail confidence < 0.7
  - Patient flags: pregnant, pediatric, elderly (≥ 80), terminal diagnosis
  - Drug interaction severity D or X
  - Mental health crisis indicators
  - Medication dosage change recommendations
- [ ] Build clinician review dashboard (approve / modify / reject workflow)
- [ ] Add fairness monitoring job over anonymized aggregate data (async)
- [ ] Implement `FairnessMonitor` for recommendation parity across demographic groups

### Tests

- [ ] Guardrail hard-block tests (diagnosis, medication change, certainty claims)
- [ ] Soft-flag disclaimer injection tests
- [ ] Human-review trigger matrix tests
- [ ] Review workflow API tests (approve, modify, reject)
- [ ] Fairness job tests with synthetic demographic distributions

### Documentation

- [ ] `docs/ai-governance.md` — responsible AI pillars, reasoning capture
- [ ] `docs/medical-guardrails.md` — hard blocks, soft flags, confidence thresholds
- [ ] `docs/human-review-workflow.md` — triggers, dashboard, SLA

---

## Phase 8: Security, Compliance, and Deployment

**Goal:** Production-ready deployment with compliance evidence for HIPAA, GDPR, SOC 2.

**Timeline:** Weeks 21–26 (per architecture doc Phase 5)

### Implementation Tasks

- [ ] Implement KMS abstraction and per-tenant encryption key lifecycle
- [ ] Add secrets management (Vault / AWS Secrets Manager)
- [ ] Container hardening: distroless base, Trivy scan on every build
- [ ] SBOM generation (CycloneDX), pip-audit, SAST (Semgrep health rules), DAST (OWASP ZAP)
- [ ] Terraform/Pulumi for AWS reference topology (see architecture doc §12)
- [ ] Zero-trust network: WAF → API Gateway → mTLS service mesh → private data subnet
- [ ] Compliance evidence collection:
  - HIPAA risk assessment + remediation
  - SOC 2 Type II audit engagement
  - GDPR data mapping document
  - Penetration test + remediation
  - Business Associate Agreements with all vendors
  - Staff training (HIPAA, data handling)

### Tests

- [ ] Secret scanning in CI (no secrets in code)
- [ ] Dependency audit and SBOM verification
- [ ] SAST custom rule tests for PHI logging and unsafe LLM calls
- [ ] DAST smoke tests against staging
- [ ] Backup/restore and disaster recovery drills

### Documentation

- [ ] `docs/security-architecture.md` — zero-trust, encryption hierarchy
- [ ] `docs/compliance-controls.md` — HIPAA/GDPR/SOC 2 mapping
- [ ] `docs/deployment/aws.md` — reference topology, cost model
- [ ] `docs/backup-restore.md` — RTO/RPO, procedures
- [ ] `docs/incident-response.md` — PHI breach, service outage

---

## Task Summary by Category

| Category | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 | Phase 7 | Phase 8 |
|----------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| Implementation | 3 | 9 | 9 | 7 | 7 | 7 | 8 | 7 | 7 |
| Tests | 3 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Documentation | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 5 |

---

## References

- [Enterprise Architecture Blueprint](../docs/enterprise-architecture.md)
- [Architecture & Developer Guide](../docs/architecture.md)
- [Implementation Roadmap](../todo/implementation-roadmap.md)

---

*Document version: 1.0 — June 2026*  
*Maintained by: SynapseMD Platform Team*
