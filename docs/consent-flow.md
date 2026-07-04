# Consent Flow

## Org intelligence RAG

Org-specific knowledge (`source_type=org_intelligence`) is **opt-in per request**:

- MCP: `search_clinical_knowledge` with `include_org_intelligence: true`
- Default: `ORG_INTELLIGENCE_ENABLED=false` in production ConfigMap
- Tenant must enable org intelligence in tenant settings before ingestion

**Consent requirement**: Tenant admin acknowledges org documents may contain internal clinical protocols and staff must not upload patient-identifiable content.

## LLM calls

Before any command reaches an external LLM provider:

1. Context is anonymized (`AnonymizationEngine`)
2. User JWT implies consent to platform ToS (document in tenant onboarding)
3. Production requires signed BAA with provider ([baa-tracking.md](baa-tracking.md))

## AI Module 21

- `/ai` and `/api/v1/ai/*` return `disclaimer` on every response
- High-risk predictions flag `human_review_required`
- Chat queries are anonymized before processing

## Data export / erasure

- Export: `GET /admin/export/{user_id}` (admin scope, tenant-scoped)
- Erasure: `POST /admin/users/{user_id}/erase` — deletes FHIR bundle, marks user `erased`

Users may request export/erasure through tenant admin per GDPR/HIPAA policy.
