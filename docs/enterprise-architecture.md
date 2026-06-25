# WellAlly-Health: Enterprise Architecture Blueprint

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Multi-Tenant Data Architecture](#3-multi-tenant-data-architecture)
4. [Regulatory Compliance Framework](#4-regulatory-compliance-framework)
5. [PII & PHI Anonymization Pipeline](#5-pii--phi-anonymization-pipeline)
6. [LLM & Health AI Strategy](#6-llm--health-ai-strategy)
7. [RAG Architecture for Clinical Knowledge](#7-rag-architecture-for-clinical-knowledge)
8. [AI Governance: Reasoning, Explainability & Responsible AI](#8-ai-governance-reasoning-explainability--responsible-ai)
9. [Audit & Observability](#9-audit--observability)
10. [Security Architecture](#10-security-architecture)
11. [Migration Path from Current Codebase](#11-migration-path-from-current-codebase)
12. [Reference Deployment Topology](#12-reference-deployment-topology)

---

## 1. Executive Summary

The current WellAlly-Health system is a single-user, file-based CLI tool. This document defines the enterprise architecture required to transform it into a **multi-tenant, regulatory-compliant, AI-powered health platform** suitable for healthcare organizations, insurance providers, and digital health companies.

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

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                        │
│  Web App (React)    Mobile (iOS/Android)    EHR Plugin    API Clients        │
└────────────────────────────┬────────────────────────────────────────────────┘
                             │ HTTPS / WSS
┌────────────────────────────▼────────────────────────────────────────────────┐
│                       API GATEWAY & IDENTITY                                 │
│  Rate Limiting   Auth (OAuth2/OIDC)   RBAC   Audit Logging   API Versioning │
└───────┬───────────────────┬───────────────────────┬──────────────────────────┘
        │                   │                       │
┌───────▼──────┐   ┌────────▼────────┐   ┌─────────▼──────────┐
│  Command     │   │  Skills /       │   │  Admin &           │
│  Service     │   │  Analyzer API   │   │  Compliance API    │
│  (59 cmds)   │   │  (22 analyzers) │   │  (audit, reports)  │
└───────┬──────┘   └────────┬────────┘   └─────────┬──────────┘
        │                   │                       │
┌───────▼───────────────────▼───────────────────────▼──────────────────────────┐
│                      PHI ANONYMIZATION LAYER                                  │
│  De-identification Engine   Tokenization Vault   Synthetic Data Generator     │
└───────────────────────────────────┬──────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼──────────────────────────────────────────┐
│                         AI ORCHESTRATION LAYER                                │
│                                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐   │
│  │  LLM Router      │  │  RAG Engine      │  │  AI Governance           │   │
│  │  (model select)  │  │  (clinical KB)   │  │  (explain, audit, guard) │   │
│  └────────┬─────────┘  └────────┬─────────┘  └───────────┬──────────────┘   │
│           │                     │                         │                   │
│  ┌────────▼─────────────────────▼─────────────────────────▼──────────────┐   │
│  │                        LLM Fleet                                       │   │
│  │  Claude Health  │  GPT-4o Health  │  Med-PaLM 2  │  Custom SLM        │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────┬──────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼──────────────────────────────────────────┐
│                           DATA LAYER                                          │
│                                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │  Clinical DB │  │  Vector DB   │  │  Event Store  │  │  Blob Storage  │  │
│  │  (FHIR)      │  │  (embeddings)│  │  (audit log)  │  │  (reports,imgs)│  │
│  │  PostgreSQL  │  │  Weaviate/   │  │  Kafka /      │  │  S3 / Azure    │  │
│  │  + HAPI FHIR │  │  Pinecone    │  │  Event Hubs   │  │  Blob          │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  └────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Multi-Tenant Data Architecture

### Tenancy Model

The platform supports two tenancy models:

**Model A — Org-scoped tenancy** (for hospitals, clinics, insurers)
```
Organization (Tenant)
  └── Department / Care Team
        └── Patient / User
              └── Health Records
```

**Model B — Consumer SaaS tenancy** (for direct-to-consumer health apps)
```
Individual User (Tenant)
  └── Family Members (sub-accounts)
        └── Health Records
```

### User & Data Isolation

Every health record is tagged with `{tenant_id, user_id}`. Isolation is enforced at three levels:

```
Level 1 — API Gateway (JWT claims)
  Every request must carry a JWT with:
  - sub: user_id
  - org: tenant_id
  - roles: [patient | clinician | admin | auditor]
  - scope: [read:own | read:org | write:own | admin]

Level 2 — Row-Level Security (PostgreSQL)
  CREATE POLICY user_isolation ON health_records
    USING (user_id = current_setting('app.user_id')::uuid
           AND tenant_id = current_setting('app.tenant_id')::uuid);

Level 3 — Encryption (separate keys per tenant)
  Each tenant gets a unique KMS key.
  Even a compromised DB dump cannot be decrypted without that key.
```

### FHIR-Based Clinical Data Model

Replace the current flat JSON tracker files with HL7 FHIR R4 resources — the international standard for health data interoperability:

| Current JSON File | FHIR Resource |
|---|---|
| `profile.json` | `Patient` |
| `allergies.json` | `AllergyIntolerance` |
| `medications/*.json` | `MedicationRequest` + `MedicationAdministration` |
| `*-tracker.json` | `Observation` (with LOINC codes) |
| `fitness-logs/` | `Observation` (LOINC 55423-8: steps, 41950-7: exercise) |
| `radiation-records.json` | `ImagingStudy` + `Observation` |
| `surgery-records/` | `Procedure` |
| `discharge-summaries/` | `Composition` (LOINC 18842-5) |
| `interactions/` | `ClinicalUseDefinition` |

```json
// Example: allergies.json → FHIR AllergyIntolerance
{
  "resourceType": "AllergyIntolerance",
  "id": "allergy-001",
  "patient": { "reference": "Patient/{user_id}" },
  "code": {
    "coding": [{
      "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
      "code": "7980",
      "display": "Penicillin"
    }]
  },
  "criticality": "high",
  "reaction": [{
    "manifestation": [{
      "coding": [{ "system": "http://snomed.info/sct", "code": "271807003", "display": "Skin rash" }]
    }],
    "severity": "severe"
  }]
}
```

**Deployment options for FHIR server:**
- **AWS:** Amazon HealthLake (managed FHIR R4)
- **Azure:** Azure Health Data Services (FHIR Service)
- **GCP:** Cloud Healthcare API (FHIR store)
- **Self-hosted:** HAPI FHIR Server on Kubernetes

### Database Schema (Non-FHIR operational data)

```sql
-- Tenant registry
CREATE TABLE tenants (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  plan        TEXT CHECK (plan IN ('starter', 'professional', 'enterprise')),
  kms_key_id  TEXT NOT NULL,           -- per-tenant encryption key
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- Users (no PHI stored here — PHI lives in FHIR)
CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id   UUID REFERENCES tenants(id),
  email_hash  TEXT NOT NULL,           -- hashed, never plaintext
  role        TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT now(),
  UNIQUE(tenant_id, email_hash)
);

-- Tokenization map (maps PHI tokens to real values, stored in separate vault)
CREATE TABLE phi_tokens (
  token       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES users(id),
  field_type  TEXT,                    -- 'name', 'dob', 'ssn', 'address'
  -- actual value stored encrypted in Vault, never here
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- AI interaction log (for audit, explainability)
CREATE TABLE ai_interactions (
  id              UUID PRIMARY KEY,
  user_id         UUID REFERENCES users(id),
  tenant_id       UUID REFERENCES tenants(id),
  command         TEXT,
  model_used      TEXT,
  prompt_hash     TEXT,                -- hash only, never store PHI prompts
  response_hash   TEXT,
  reasoning_trace JSONB,              -- chain-of-thought captured
  latency_ms      INTEGER,
  tokens_in       INTEGER,
  tokens_out      INTEGER,
  safety_flags    JSONB,
  created_at      TIMESTAMPTZ DEFAULT now()
) PARTITION BY RANGE (created_at);    -- partition by month for retention
```

---

## 4. Regulatory Compliance Framework

### HIPAA Technical Safeguards Mapping

| HIPAA Requirement | Implementation |
|---|---|
| Access Control (§164.312(a)(1)) | JWT + RBAC + row-level security |
| Audit Controls (§164.312(b)) | Immutable event log (Kafka → S3 Glacier) |
| Integrity (§164.312(c)(1)) | FHIR resource versioning + SHA-256 checksums |
| Transmission Security (§164.312(e)(1)) | TLS 1.3 everywhere, mTLS between services |
| Encryption at Rest | AES-256, per-tenant KMS keys (AWS KMS / Azure Key Vault) |
| PHI Minimum Necessary | PHI anonymized before LLM; tokenized in all logs |
| Business Associate Agreements | Required with all subprocessors (cloud, LLM providers) |

### GDPR / Data Protection Mapping

| Right | Implementation |
|---|---|
| Right of Access | `/admin/export/{user_id}` returns full FHIR bundle |
| Right to Erasure | Soft-delete + scheduled hard-delete job; revoke KMS key |
| Right to Portability | FHIR R4 export (`.ndjson`) |
| Data Minimization | Anonymization layer strips all direct identifiers before analysis |
| Consent Management | Consent FHIR resource; every LLM call checks active consent |
| Data Residency | Per-tenant deployment region configuration |

### SOC 2 Type II Controls

```
CC6 — Logical Access:    MFA required, SSO via SAML/OIDC, zero-standing-privilege
CC7 — System Operations: Automated vulnerability scanning, patch SLAs
CC8 — Change Management: GitOps deployment, PR approvals, signed commits
CC9 — Risk Mitigation:   Penetration testing (annual), bug bounty program
A1  — Availability:      Multi-AZ deployment, 99.9% SLA, chaos engineering
C1  — Confidentiality:   PHI never in logs, anonymization enforced at build time
PI1 — Processing Integrity: LLM outputs validated against medical guardrails
```

### HL7 FHIR Conformance

- All clinical data stored as FHIR R4 resources
- SMART on FHIR for EHR integration (Epic, Cerner, Meditech)
- LOINC codes for observations, RxNorm for medications, SNOMED CT for diagnoses
- CDS Hooks for real-time clinical decision support integration

---

## 5. PII & PHI Anonymization Pipeline

This is the most critical compliance layer. **PHI must never reach the LLM in its raw form.**

### De-identification Approaches

**HIPAA Safe Harbor Method** — remove 18 specific identifiers:
```
Names, Geographic data (< state level), Dates (except year),
Phone numbers, Fax numbers, Email addresses, SSN, Medical record numbers,
Health plan beneficiary numbers, Account numbers, Certificate/license numbers,
Vehicle identifiers, Device identifiers, Web URLs, IP addresses,
Biometric identifiers, Full-face photographs, Any unique identifying numbers
```

**Expert Determination Method** — statistical risk < 0.04 re-identification probability (used for research/analytics pipelines).

### Anonymization Pipeline Architecture

```
Raw Health Record (PHI)
        │
        ▼
┌───────────────────────────────────────┐
│  Step 1: NER-based PHI Detection      │
│  Model: AWS Comprehend Medical /      │
│  Microsoft Presidio / custom NER      │
│  Detects: names, DOB, addresses,      │
│  MRNs, phone numbers in free text     │
└────────────────────┬──────────────────┘
                     │
        ▼
┌───────────────────────────────────────┐
│  Step 2: Tokenization                 │
│  Replace PHI with stable tokens:      │
│  "John Smith" → {TOKEN:patient:a3f2}  │
│  "1990-05-15" → {TOKEN:dob:b7c1}     │
│  Token ↔ Real value stored in         │
│  HashiCorp Vault (separate service)   │
└────────────────────┬──────────────────┘
                     │
        ▼
┌───────────────────────────────────────┐
│  Step 3: Generalization               │
│  Specific dates → age ranges           │
│  ZIP codes → region codes              │
│  Rare conditions → category codes     │
└────────────────────┬──────────────────┘
                     │
        ▼
┌───────────────────────────────────────┐
│  Step 4: Validation                   │
│  Re-run NER detector on output        │
│  Assert zero PHI tokens remain        │
│  If PHI detected → block + alert      │
└────────────────────┬──────────────────┘
                     │
        ▼
   Anonymized record → LLM
```

### Implementation: Microsoft Presidio Integration

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def anonymize_for_llm(text: str, user_id: str) -> tuple[str, dict]:
    """Returns (anonymized_text, token_map) for later de-anonymization."""
    
    results = analyzer.analyze(
        text=text,
        entities=["PERSON", "DATE_TIME", "LOCATION", "PHONE_NUMBER",
                  "EMAIL_ADDRESS", "MEDICAL_LICENSE", "US_SSN", "US_ITIN"],
        language="en"
    )
    
    # Replace with stable tokens (reversible for clinician view)
    token_map = {}
    operators = {}
    for result in results:
        token = f"TOKEN_{result.entity_type}_{generate_stable_id(user_id, result)}"
        token_map[token] = text[result.start:result.end]
        operators[result.entity_type] = OperatorConfig("replace", {"new_value": token})
    
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
    return anonymized.text, token_map

def deanonymize_response(text: str, token_map: dict) -> str:
    """Restore tokens in LLM response back to real values for authorized users."""
    for token, real_value in token_map.items():
        text = text.replace(token, real_value)
    return text
```

### PHI Handling Rules by Data Path

```
User → API           PHI allowed (TLS encrypted, authenticated)
API → LLM            PHI NEVER sent — always anonymized first
API → Database       PHI encrypted at rest with tenant KMS key
API → Logs           PHI NEVER in logs — only tokens and hashes
LLM → User           Tokens in LLM output de-anonymized for authorized users
Audit logs           Token references only (no PHI), immutable append-only
Analytics/Research   Expert-determination de-identification, k-anonymity ≥ 5
```

---

## 6. LLM & Health AI Strategy

### Model Selection Framework

Not all health tasks require the same model. A routing layer selects the best model for each task:

```
Task Type                  →  Recommended Model
─────────────────────────────────────────────────────────────────
Drug interaction check     →  Rule-based + Med-PaLM 2 / BioGPT
Symptom pattern analysis   →  Claude claude-opus-4-8 / GPT-4o
Clinical report generation →  Claude claude-sonnet-4-6 (cost-efficient)
Simple data CRUD           →  Claude claude-haiku-4-5 (fast, cheap)
Radiology report parsing   →  Med-Gemini / specialized vision model
Mental health screening    →  Custom fine-tuned + human review required
TCM consultation           →  Org-specific fine-tuned SLM
Triage / urgent flags      →  Fast local SLM (latency < 200ms)
Population analytics       →  Batch processing, cost-optimized models
```

### Health-Specialized Models

| Model | Provider | Strength | Use Case |
|---|---|---|---|
| **Claude claude-opus-4-8** | Anthropic | Reasoning, safety, long context | Complex consultations, MDT reports |
| **GPT-4o** | OpenAI | Multimodal (image + text) | Medical image + report analysis |
| **Med-PaLM 2** | Google | Clinical Q&A, medical knowledge | Drug interactions, clinical guidelines |
| **Med-Gemini** | Google | Multimodal medical | Radiology, pathology images |
| **BioGPT** | Microsoft | Biomedical literature | Research synthesis, evidence retrieval |
| **Meditron-70B** | EPFL (open) | General clinical, self-hostable | On-premise deployment, cost control |
| **PMC-LLaMA** | Stanford (open) | Medical literature trained | RAG over clinical documents |
| **Custom SLM** | Org fine-tuned | Org-specific workflows | Proprietary protocols, local dialect |

### LLM Router Implementation

```python
from enum import Enum
from dataclasses import dataclass

class TaskComplexity(Enum):
    SIMPLE = "simple"        # CRUD, formatting
    MODERATE = "moderate"    # Analysis, summarization
    COMPLEX = "complex"      # Multi-step reasoning, consultation
    CRITICAL = "critical"    # Safety-sensitive, requires validation

class DataSensitivity(Enum):
    ANONYMIZED = "anonymized"
    PSEUDONYMIZED = "pseudonymized"

@dataclass
class RoutingDecision:
    model: str
    provider: str
    max_tokens: int
    temperature: float
    require_human_review: bool
    fallback_model: str

class HealthLLMRouter:
    
    ROUTING_TABLE = {
        ("simple",   "anonymized"):      RoutingDecision("claude-haiku-4-5", "anthropic", 1024, 0.1, False, "gpt-4o-mini"),
        ("moderate", "anonymized"):      RoutingDecision("claude-sonnet-4-6", "anthropic", 4096, 0.2, False, "gpt-4o"),
        ("complex",  "anonymized"):      RoutingDecision("claude-opus-4-8",  "anthropic", 8192, 0.3, False, "gpt-4o"),
        ("critical", "anonymized"):      RoutingDecision("claude-opus-4-8",  "anthropic", 8192, 0.1, True,  "med-palm-2"),
        # pseudonymized data stays on approved health AI providers only
        ("moderate", "pseudonymized"):   RoutingDecision("med-palm-2", "google-health", 4096, 0.2, False, "meditron-70b"),
        ("complex",  "pseudonymized"):   RoutingDecision("med-palm-2", "google-health", 8192, 0.1, True,  "meditron-70b"),
    }
    
    def route(self, command: str, data_sensitivity: str, context_size: int) -> RoutingDecision:
        complexity = self._assess_complexity(command, context_size)
        key = (complexity.value, data_sensitivity)
        return self.ROUTING_TABLE.get(key, self._default_safe_route())
    
    def _assess_complexity(self, command: str, context_size: int) -> TaskComplexity:
        CRITICAL_COMMANDS = {"consult", "specialist", "mental-health", "psych-assess"}
        COMPLEX_COMMANDS = {"report", "ai", "health-trend-analyzer", "interaction"}
        SIMPLE_COMMANDS = {"profile", "query", "get-profile"}
        
        if command in CRITICAL_COMMANDS:
            return TaskComplexity.CRITICAL
        if command in COMPLEX_COMMANDS or context_size > 10000:
            return TaskComplexity.COMPLEX
        if command in SIMPLE_COMMANDS and context_size < 2000:
            return TaskComplexity.SIMPLE
        return TaskComplexity.MODERATE
```

### On-Premise / Air-Gapped Deployment (Highly Regulated Orgs)

For organizations that cannot send data to cloud LLM providers (e.g., military health, certain EU jurisdictions):

```
┌─────────────────────────────────────────────────┐
│  On-Premise GPU Cluster                         │
│                                                 │
│  ┌─────────────┐    ┌──────────────────────┐   │
│  │ Meditron-70B│    │  Custom Fine-tuned   │   │
│  │ (EPFL)      │    │  SLM (org-specific)  │   │
│  │ 4× A100 GPU │    │  2× A100 GPU         │   │
│  └─────────────┘    └──────────────────────┘   │
│                                                 │
│  Served via: vLLM / Ollama / TGI               │
│  API: OpenAI-compatible (/v1/chat/completions) │
└─────────────────────────────────────────────────┘
```

The LLM router simply points to the internal endpoint — all command/skill definitions remain unchanged.

---

## 7. RAG Architecture for Clinical Knowledge

### Why RAG for Health AI

Raw LLM knowledge has a training cutoff and cannot access:
- Your organization's clinical protocols
- Recent drug approvals / recalls
- Hospital formulary (which drugs are stocked)
- Payer-specific coverage rules
- Local epidemiological data

RAG (Retrieval-Augmented Generation) grounds LLM responses in authoritative, current knowledge.

### Clinical Knowledge Base Sources

```
┌────────────────────────────────────────────────────────────┐
│                  Clinical Knowledge Base                    │
│                                                            │
│  Public Sources (ingested + chunked + embedded):           │
│  ├── PubMed abstracts (37M papers via E-utilities API)     │
│  ├── FDA drug labels (DailyMed, openFDA)                   │
│  ├── WHO ICD-11 coding system                              │
│  ├── Clinical practice guidelines (AHA, ADA, USPSTF, etc.) │
│  ├── CDC vaccine schedules                                 │
│  └── SNOMED CT / LOINC / RxNorm ontologies                 │
│                                                            │
│  Org-Specific Sources (private, per-tenant):               │
│  ├── Hospital formulary                                    │
│  ├── Internal clinical protocols & pathways                │
│  ├── Payer coverage policies                               │
│  ├── Anonymized historical patient outcomes                │
│  └── Physician notes (de-identified, for SLM fine-tuning) │
└────────────────────────────────────────────────────────────┘
```

### RAG Pipeline

```
Query (anonymized)
      │
      ▼
┌──────────────────────────────────────────────────────────┐
│  Step 1: Query Understanding                              │
│  Extract intent, medical entities (symptoms, drugs,       │
│  conditions), and required knowledge domains              │
│  Tool: MedSpaCy NER + UMLS concept normalization          │
└───────────────────────────┬──────────────────────────────┘
                            │
      ▼
┌──────────────────────────────────────────────────────────┐
│  Step 2: Hybrid Retrieval                                 │
│                                                          │
│  ┌─────────────────┐    ┌────────────────────────────┐  │
│  │ Semantic Search │    │  Keyword / BM25 Search     │  │
│  │ (vector sim.)   │    │  (exact medical terms)     │  │
│  │ Weaviate /      │    │  Elasticsearch /           │  │
│  │ Pinecone        │    │  OpenSearch                │  │
│  └────────┬────────┘    └─────────────┬──────────────┘  │
│           └─────────────┬─────────────┘                  │
│                         ▼                                 │
│              Reciprocal Rank Fusion                       │
│              (merge + re-rank results)                    │
└───────────────────────────┬──────────────────────────────┘
                            │
      ▼
┌──────────────────────────────────────────────────────────┐
│  Step 3: Relevance Filtering & Citation Extraction        │
│  - Cross-encoder re-ranking (top 10 → top 3)             │
│  - Extract source DOI, guideline name, evidence level     │
│  - Flag outdated sources (> 5 years for rapidly evolving  │
│    fields; > 10 years for stable guidelines)              │
└───────────────────────────┬──────────────────────────────┘
                            │
      ▼
┌──────────────────────────────────────────────────────────┐
│  Step 4: Context Injection                                │
│  Prepend retrieved chunks to LLM prompt:                  │
│  SYSTEM: You are a health AI. Use ONLY the following      │
│  verified clinical sources to answer. Cite each claim.   │
│  [Source 1: AHA 2023 Hypertension Guidelines, p.14]...   │
└───────────────────────────┬──────────────────────────────┘
                            │
      ▼
   LLM Response with inline citations
```

### Embedding Strategy for Medical Text

```python
from sentence_transformers import SentenceTransformer

# Health-specific embedding model outperforms generic models on clinical text
model = SentenceTransformer("pritamdeka/S-PubMedBert-MS-MARCO")
# Alternative: "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract"

def embed_clinical_document(text: str, doc_id: str, source: str) -> dict:
    embedding = model.encode(text, normalize_embeddings=True)
    return {
        "id": doc_id,
        "vector": embedding.tolist(),
        "metadata": {
            "source": source,
            "evidence_level": extract_evidence_level(text),  # A/B/C/D
            "publication_date": extract_date(text),
            "specialty": classify_specialty(text),
        }
    }
```

---

## 8. AI Governance: Reasoning, Explainability & Responsible AI

### Responsible AI Framework

```
┌────────────────────────────────────────────────────────────┐
│              Responsible AI Pillars                        │
│                                                            │
│  Fairness     │ Bias detection across age/gender/race      │
│  Reliability  │ Confidence scores, uncertainty quantify    │
│  Safety       │ Medical guardrails, harm detection         │
│  Privacy      │ PHI anonymization (see §5)                 │
│  Inclusiveness│ Multi-language, accessibility              │
│  Transparency │ Explainability, reasoning traces           │
│  Accountability│ Human-in-the-loop, audit trail            │
└────────────────────────────────────────────────────────────┘
```

### Reasoning Capture (Chain-of-Thought Audit)

For every AI interaction that influences a health decision, capture the full reasoning trace:

```python
@dataclass
class ReasoningTrace:
    interaction_id: str
    command: str
    
    # What data was considered
    data_sources_read: list[str]          # ["data/medications.json", "data/allergies.json"]
    rag_sources_retrieved: list[Citation]  # Clinical guidelines, papers
    
    # How the AI reasoned
    thinking_steps: list[str]             # CoT steps (from extended thinking)
    assumptions_made: list[str]           # Explicit assumptions stated
    alternatives_considered: list[str]    # Other conclusions the model considered
    
    # What the AI concluded
    conclusion: str
    confidence_level: float               # 0.0 - 1.0
    uncertainty_factors: list[str]        # What would change the conclusion
    
    # Safety checks performed
    safety_checks: list[SafetyCheckResult]
    contraindications_checked: bool
    human_review_required: bool
    
    # Metadata
    model_id: str
    model_version: str
    timestamp: datetime
    latency_ms: int
```

**Enable extended thinking for Claude** to capture CoT:
```python
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Allow deep reasoning for clinical decisions
    },
    messages=[{"role": "user", "content": anonymized_prompt}]
)

# Extract and store the thinking block
for block in response.content:
    if block.type == "thinking":
        reasoning_trace.thinking_steps = parse_thinking(block.thinking)
    elif block.type == "text":
        reasoning_trace.conclusion = block.text
```

### Medical Guardrails

Every LLM response passes through a guardrail layer before reaching the user:

```python
class MedicalGuardrails:
    
    HARD_BLOCKS = [
        "prescribe|diagnose|you have|you are suffering",  # Diagnosis claims
        "stop taking|discontinue your medication",         # Medication changes
        "emergency|call 911",                              # Emergency handling (use structured flow)
        "guarantee|cure|100%",                             # Certainty claims
    ]
    
    SOFT_FLAGS = [
        "recommend|suggest|should",     # Adds disclaimer
        "study shows|research found",   # Requires citation check
        "rare|unusual|uncommon",        # Triggers confidence check
    ]
    
    def validate(self, response: str, command: str, reasoning_trace: ReasoningTrace) -> GuardrailResult:
        
        # Hard blocks — response never reaches user
        for pattern in self.HARD_BLOCKS:
            if re.search(pattern, response, re.IGNORECASE):
                return GuardrailResult(
                    blocked=True,
                    reason=f"Response contains prohibited pattern: {pattern}",
                    safe_fallback=self._get_safe_fallback(command)
                )
        
        # Confidence threshold — low confidence triggers human review
        if reasoning_trace.confidence_level < 0.7:
            return GuardrailResult(
                blocked=False,
                requires_disclaimer=True,
                disclaimer="This analysis has limited confidence. Please consult a healthcare provider.",
                human_review_queued=True
            )
        
        # Citation requirement for clinical claims
        if any(flag in response for flag in ["study", "guideline", "evidence"]):
            if not reasoning_trace.rag_sources_retrieved:
                return GuardrailResult(
                    blocked=False,
                    requires_disclaimer=True,
                    disclaimer="Clinical claims require verification with your healthcare provider."
                )
        
        return GuardrailResult(blocked=False)
```

### Fairness & Bias Detection

```python
class FairnessMonitor:
    """
    Detects systematic disparities in AI recommendations across
    demographic groups. Runs asynchronously on aggregated, anonymized data.
    """
    
    PROTECTED_ATTRIBUTES = ["age_group", "biological_sex", "condition_severity"]
    
    def compute_recommendation_parity(self, 
                                       recommendations: list[Recommendation],
                                       window_days: int = 30) -> FairnessReport:
        """
        For each command type, compute whether recommendations differ
        systematically across demographic groups.
        Flags if difference > 2 standard deviations from mean.
        """
        ...
    
    def detect_representation_gap(self, rag_results: list[Citation]) -> list[str]:
        """
        Checks if retrieved clinical literature adequately represents
        diverse populations. Flags if > 80% of sources study only
        one demographic group.
        """
        ...
```

### Human-in-the-Loop Workflow

Certain actions always require human (clinician) review before the response reaches the patient:

```
Triggers for human review:
  - Command is /consult, /specialist (MDT consultation)
  - Guardrail confidence < 0.7
  - Patient flags: pregnant, pediatric, elderly (≥ 80), terminal diagnosis
  - Drug interaction severity = D or X (ALWAYS block + escalate)
  - Mental health crisis indicators detected
  - Any recommendation to change medication dosage

Review workflow:
  Patient request
       │
       ▼
  AI generates response + reasoning trace
       │
       ▼  (if human review triggered)
  Response held in review queue
       │
       ▼
  Clinician reviews in review dashboard (shows AI reasoning, sources)
       │
       ├──(approve)──▶ Response sent to patient + audit logged
       ├──(modify)───▶ Clinician edits response → sent + audit logged
       └──(reject)───▶ Safe fallback message → patient notified
```

---

## 9. Audit & Observability

### Immutable Audit Log

Every PHI access, AI interaction, and data modification is written to an append-only event log:

```json
{
  "event_id": "evt_01HXYZ...",
  "event_type": "ai.command.executed",
  "timestamp": "2025-06-25T10:30:00.000Z",
  "actor": {
    "user_id": "usr_token_a3f2",
    "tenant_id": "org_hospital_xyz",
    "role": "patient",
    "ip_hash": "sha256:abc123..."
  },
  "resource": {
    "command": "allergy",
    "action": "list",
    "data_files_accessed": ["data/allergies.json"],
    "phi_tokens_involved": ["TOKEN_PATIENT_a3f2"]
  },
  "ai": {
    "model": "claude-sonnet-4-6",
    "interaction_id": "int_01HABC...",
    "tokens_consumed": 1240,
    "latency_ms": 850,
    "safety_flags": [],
    "confidence": 0.92
  },
  "outcome": "success",
  "signature": "hmac_sha256:..."
}
```

Events stream to: **Kafka → S3 Glacier** (7-year HIPAA retention) and are indexed in **OpenSearch** for real-time querying.

### Observability Stack

```
┌──────────────────────────────────────────────────────┐
│               Observability Stack                     │
│                                                      │
│  Metrics:   Prometheus → Grafana                     │
│  Traces:    OpenTelemetry → Jaeger / Tempo           │
│  Logs:      Structured JSON → Loki / CloudWatch      │
│  Audit:     Kafka → S3 Glacier (immutable)           │
│  Alerts:    PagerDuty / OpsGenie                     │
│                                                      │
│  Health-Specific Dashboards:                         │
│  - LLM token consumption by command                  │
│  - Guardrail trigger rate (% blocked)                │
│  - Human review queue depth + SLA breach alerts      │
│  - PHI tokenization failure rate (must be 0%)        │
│  - Model drift: response quality score over time     │
│  - RAG retrieval relevance scores                    │
│  - Per-tenant API latency p50/p95/p99                │
└──────────────────────────────────────────────────────┘
```

### Data Lineage Tracking

Every piece of data that influences an AI response is tracked end-to-end:

```
User's allergy record (created 2024-01-15)
  └── Read by /consult command (2025-06-25T10:30)
        └── Anonymized by Presidio v2.3.1
              └── Embedded as context for claude-opus-4-8
                    └── RAG retrieved: AHA 2023 Guidelines §4.2
                          └── AI response generated (interaction_id: int_01H...)
                                └── Passed guardrail check (confidence: 0.91)
                                      └── Delivered to user (audit: evt_01H...)
```

---

## 10. Security Architecture

### Zero-Trust Network Model

```
Internet → WAF (AWS Shield / Cloudflare) → API Gateway
                                                │
                            ┌───────────────────┼──────────────────┐
                            │                   │                  │
                    Service Mesh (mTLS between all services)       │
                            │                   │                  │
                    Command Service     Skill Service     Admin API
                            │
                    ┌───────▼─────────────────────────────┐
                    │  Data Layer (private subnet, no      │
                    │  internet access, VPC-only)          │
                    │  PostgreSQL | FHIR | Vector DB        │
                    └──────────────────────────────────────┘
```

### Encryption Key Hierarchy

```
AWS KMS Master Key (HSM-backed, org-level)
  └── Tenant Data Encryption Key (DEK, one per tenant)
        └── Record Encryption Key (REK, rotated quarterly)
              └── Encrypted PHI fields in database

PHI Token Vault (HashiCorp Vault — separate deployment)
  └── Token → Real Value mapping (access requires separate auth)
  └── Accessed only by: anonymization service, authorized clinicians
```

### Dependency & Supply Chain Security

```
- All Docker images: distroless base, vulnerability scan on every build (Trivy)
- Python deps: pip-audit + SBOM generation (CycloneDX)
- LLM provider SDKs: pinned versions, hash verification
- Secrets: never in code; Vault / AWS Secrets Manager only
- SAST: Semgrep (custom rules for health data handling)
- DAST: OWASP ZAP on every release
- Pen test: annual third-party + continuous bug bounty
```

---

## 11. Migration Path from Current Codebase

### Phase 1 — Foundation (Weeks 1–4): Auth + Multi-Tenancy

```
✓ Deploy API Gateway (Kong / AWS API GW)
✓ Integrate identity provider (Auth0 / Cognito / Keycloak)
✓ Implement JWT validation + RBAC middleware
✓ Create tenant registry and user tables
✓ Wrap existing commands in REST endpoints (thin adapter)
✓ All existing command .md files remain unchanged
```

### Phase 2 — PHI Safety (Weeks 5–8): Anonymization Pipeline

```
✓ Deploy Microsoft Presidio (anonymization service)
✓ Intercept all LLM calls → anonymize before → de-anonymize after
✓ Deploy HashiCorp Vault for token storage
✓ Implement audit event logging (Kafka)
✓ Validate: zero PHI reaches LLM in staging environment
```

### Phase 3 — Data Migration (Weeks 9–16): File → FHIR

```
✓ Deploy HAPI FHIR Server (or HealthLake)
✓ Build migration scripts: JSON trackers → FHIR resources
✓ Update commands to read/write FHIR instead of local JSON
  (abstract behind a DataAccessLayer so command .md logic unchanged)
✓ Deploy vector database (Weaviate)
✓ Ingest clinical knowledge base (PubMed, FDA, guidelines)
✓ Enable RAG for consultation and analysis commands
```

### Phase 4 — AI Governance (Weeks 17–20)

```
✓ Implement LLM Router (model selection)
✓ Add extended thinking / CoT capture for complex commands
✓ Deploy guardrail validation layer
✓ Build human review dashboard
✓ Implement fairness monitoring (async)
✓ Enable per-response confidence scoring
```

### Phase 5 — Compliance Certification (Weeks 21–26)

```
✓ HIPAA risk assessment + remediation
✓ SOC 2 Type II audit engagement
✓ GDPR data mapping document
✓ Penetration test + remediation
✓ Business Associate Agreements with all vendors
✓ Staff training (HIPAA, data handling)
```

---

## 12. Reference Deployment Topology

### AWS Reference Architecture

```
┌─────────────────── AWS Region (us-east-1) ─────────────────────────────┐
│                                                                         │
│  ┌── Public Subnet ──────────────────────────────────────────────────┐ │
│  │  CloudFront CDN → WAF → ALB → ECS Fargate (API Gateway service)   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌── Private Subnet (app tier) ──────────────────────────────────────┐ │
│  │  ECS Fargate:                                                      │ │
│  │  ├── command-service (auto-scaled, 2-20 tasks)                    │ │
│  │  ├── skill-service (GPU-optional for local SLM)                   │ │
│  │  ├── anonymization-service (Presidio)                             │ │
│  │  ├── rag-service (retrieval + embedding)                          │ │
│  │  └── audit-service (Kafka producer)                               │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌── Private Subnet (data tier — no internet) ────────────────────── ┐ │
│  │  Amazon HealthLake (FHIR R4)                                      │ │
│  │  Amazon Aurora PostgreSQL (operational data, RLS enabled)         │ │
│  │  Amazon OpenSearch (audit log index)                               │ │
│  │  Amazon MSK (Kafka — audit event streaming)                       │ │
│  │  Amazon S3 Glacier (7-year audit retention)                       │ │
│  │  Amazon Weaviate via ECS (vector DB — in VPC)                     │ │
│  │  HashiCorp Vault on ECS (token vault)                             │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Cross-cutting:                                                         │
│  AWS KMS (per-tenant keys)  │  Secrets Manager  │  CloudTrail          │
│  AWS Shield Advanced        │  GuardDuty         │  Security Hub        │
└─────────────────────────────────────────────────────────────────────────┘

External:
  Anthropic API (Claude) — BAA required
  OpenAI API (GPT-4o)   — BAA required for healthcare
  Google Health AI       — BAA required
```

### Cost Model (Indicative, AWS)

| Component | Monthly Cost (10k users) |
|---|---|
| ECS Fargate (app tier) | ~$800 |
| Amazon HealthLake | ~$1,500 |
| Aurora PostgreSQL | ~$400 |
| MSK + S3 Glacier (audit) | ~$300 |
| Weaviate (vector DB, r6g.2xl) | ~$600 |
| LLM API calls (Claude Sonnet) | ~$2,000–8,000 |
| KMS + Secrets Manager | ~$100 |
| WAF + Shield | ~$200 |
| **Total** | **~$6,000–15,000/mo** |

> LLM cost dominates. Use Haiku for simple commands, cache RAG embeddings, and enable prompt caching for repeated system prompts to reduce cost by 60–80%.

---

*Document version: 1.0 — June 2025*
*Maintained by: WellAlly Tech Platform Team*
