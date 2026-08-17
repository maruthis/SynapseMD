# Consent Flow

## Org intelligence RAG

Org-specific knowledge (`source_type=org_intelligence`) is **opt-in per request**:

- MCP: `search_clinical_knowledge` with `include_org_intelligence: true`
- Default: `ORG_INTELLIGENCE_ENABLED=false` in production ConfigMap
- Tenant must enable org intelligence in tenant settings before ingestion

**Consent requirement**: Tenant admin acknowledges org documents may contain internal clinical protocols and staff must not upload patient-identifiable content.

## LLM calls

Before any command reaches an external LLM provider:

1. **Consent** — `llm_processing` must be granted (`PUT /api/v1/auth/consent`). Development defaults to granted when no row exists; staging/prod require an explicit grant.
2. Context is anonymized (`AnonymizationEngine`)
3. The coded PDP (`auth/policy.py`) denies the LLM path when consent is false (`403` + audit `authz.denied`)
4. Production requires signed BAA with provider ([baa-tracking.md](baa-tracking.md))

Health-data CRUD (`profile` / `allergy` / `gout`) does **not** require `llm_processing` consent. Consent rows include `source` (default `implicit`) and optional `expires_at` (Alembic `0007_consent_columns` on existing Compose volumes).

## Identity (Phase B)

| Path | When |
|------|------|
| Password `/auth/login` | `APP_ENV=development` only |
| OIDC `/auth/oidc/login` + callback / token exchange | Staging/prod primary; PKCE for BFF, JWT bearer for API/MCP |
| Refresh `/auth/refresh` | Rotating opaque refresh token (15-minute access JWT) |
| Break-glass `/auth/break-glass` | Clinician/admin; time-boxed; extra audit + notify stub |

Browsers may set an HttpOnly refresh cookie when `AUTH_BFF_COOKIES=true`. MCP and API clients use `Authorization: Bearer` only — no long-lived PAT in tool logs.

## AI Module 21

- `/ai` and `/api/v1/ai/*` return `disclaimer` on every response
- High-risk predictions flag `human_review_required`
- Chat queries are anonymized before processing

## Data export / erasure

- Privacy officer DSR: `POST /privacy/dsr` with `access` / `erase` / `correct` (scope `privacy`)
- Completion certificate is identifiers + counts only (no names, emails, MRN, labs)
- Legal hold: `POST /privacy/legal-hold` — blocks erase and WORM archive delete
- Legacy admin: `GET /admin/export/{user_id}`, `POST /admin/users/{user_id}/erase` (also respects legal hold)

Users may request export/erasure through the tenant privacy officer per GDPR/HIPAA policy.
