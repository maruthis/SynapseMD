# SynapseMD Enterprise Platform — Implementation Plan

**Document ID:** SYN-ARCH-ENT-002  
**Status:** Complete — Phases A–E shipped (A-1–A-11, B-1–B-11, C-1–C-12, D-1–D-12, E-1–E-10). Live staging PITR/rollback remain operator-owned drills.  
**Date:** 2026-08-17  
**Design basis:** [enterprise-platform-architecture.md](enterprise-platform-architecture.md) (SYN-ARCH-ENT-001)  
**Companions:** [implementation-roadmap.md](implementation-roadmap.md) · [release-gates.md](release-gates.md) · [compliance-controls.md](compliance-controls.md)

This plan turns the enterprise architecture into **buildable phases**. Domain artifacts (`commands/`, `skills/`, `specialists/`) stay markdown. Work here is **platform rails only**.

---



## 1. How to use this plan

1. Complete phases **in order A → E** unless a work item is marked *parallel-safe*.
2. Do not mark a phase done until **exit criteria** and **tests** are green.
3. Keep local IDE JSON vault working via `LegacyJsonAdapter`; never make `data/*.json` the production SoR.
4. Every phase updates: tests, [compliance-controls.md](compliance-controls.md) if a control changes, and a short threat note in the PR.
5. Indicative calendar (one platform squad): **A 4–6 w · B 4–6 w · C 3–5 w · D 4–6 w · E 4–8 w**. Adjust to staffing.



### Locked decisions (from architecture §17)


| Topic            | Decision                                                  |
| ---------------- | --------------------------------------------------------- |
| FHIR             | Postgres SoR + FHIR JSONB projection; HAPI optional later |
| Policy engine    | In-process coded PDP first (not OPA)                      |
| Browser sessions | BFF cookies in prod UIs; JWT for MCP/API                  |
| MDT on platform  | Specialist worker pool in Phase E, not A                  |
| Regions          | Single-region + DR until residency requires split         |


---



## 2. Phase overview


| Phase | Name                  | Primary outcome                                            | Depends on                                   |
| ----- | --------------------- | ---------------------------------------------------------- | -------------------------------------------- |
| **A** | Data plane            | Postgres + Alembic + RLS + HealthDataService               | Current platform (done)                      |
| **B** | Identity & access     | OIDC SSO, MFA via IdP, PDP, prod CORS                      | A (users live in Postgres)                   |
| **C** | Observability & audit | OTel, PHI-free logs, hash-chained audit, SIEM hook         | A (durable DB)                               |
| **D** | PHI & models          | Presidio default, Vault tokens, model catalog/policy       | A + B (consent/policy), C (audit of routing) |
| **E** | Privacy ops & HA      | DSR jobs, legal hold, HA/PITR drills, optional MDT workers | A–D                                          |


```text
A (data) ──► B (identity) ──► D (PHI + models)
     │              │
     └──────► C (logs/audit) ──┘
                         │
                         ▼
                    E (DSR / HA / MDT workers)
```

C can start once A’s audit table is durable (does not need SSO). D needs B’s consent/purpose claims.

---



## 3. Cross-phase quality gates

Every phase after A must pass:


| Gate                    | Rule                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| **Tenant isolation**    | Cross-tenant read/write tests fail closed (extend `tests/release/test_tenant_isolation.py`) |
| **No PHI in logs**      | Negative tests: names/MRN/lab values never appear in captured log/audit payloads            |
| **Artifacts untouched** | No requirement for SMEs to edit Python to add a command/skill/specialist                    |
| **Coverage**            | `synapsemd_platform` stays ≥95% in CI                                                       |
| **Migrations**          | Alembic upgrade/downgrade on a clean Postgres                                               |
| **Secrets**             | No new long-lived secrets in git or plaintext ConfigMaps                                    |


---



## 4. Phase A — Data plane (foundation)



### Objectives

PostgreSQL is the system of record for identity, clinical/tracker data, AI history, and audit. JSON is an import/export adapter.

### Work items


| ID   | Task                                                                                      | Primary files / location                                                   | Tests                                                            |
| ---- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| A-1  | Add Alembic; stop relying on `create_all` for schema in staging/prod                      | `platform/alembic/`, `core/database.py`                                    | Migration upgrade/downgrade in CI against Postgres service       |
| A-2  | Postgres 16 in Compose `core`/`full`; document local `DATABASE_URL`                       | `platform/docker-compose.yml`, `.env.example`, `docs/local-development.md` | Compose smoke: API starts, `/health`                             |
| A-3  | Schema packages: `iam`, `clinical`, `trackers`, `ai`, `governance` (stubs), `audit`       | `models/` split or `models/iam.py`, `clinical.py`, `trackers.py`           | Unit: model round-trip                                           |
| A-4  | RLS on **all** tenant tables; middleware `SET LOCAL app.tenant_id` / `app.user_id`        | `migrations/00x_rls.sql`, `auth/middleware.py` or `core/db_session.py`     | Release: cross-tenant SELECT/INSERT denied                       |
| A-5  | `HealthDataService` + `PostgresHealthAdapter` + `LegacyJsonAdapter`                       | `services/health_data.py`, `adapters/`                                     | Unit: adapter interface; integration: write allergy/gout/profile |
| A-6  | FHIR JSONB projection on write (Patient, AllergyIntolerance, Observation)                 | `fhir/projection.py` (extend `fhir/migration.py`)                          | Unit: JSON tracker → FHIR resource                               |
| A-7  | Object-store interface (S3-compatible) for PDFs/reports; DB stores URI + hash             | `storage/object_store.py`                                                  | Unit: mock bucket; no blob in Postgres                           |
| A-8  | Extend `POST /admin/migrate` to upsert domain tables (not only FHIR files)                | `api/routes/admin.py`, `fhir/migration.py`                                 | Integration: sample `data-example/` → rows                       |
| A-9  | Dual-read: Postgres first, JSON fallback (feature flag `HEALTH_STORE=postgres|json|dual`) | `core/config.py`, adapters                                                 | Integration: flag matrix                                         |
| A-10 | Wire Module 21 `TenantHealthDataAdapter` to Postgres                                      | `ai/data_adapter.py`                                                       | Existing AI tenant isolation tests still pass                    |
| A-11 | Command catalog table (id, sensitivity, scopes) seeded from `AVAILABLE_COMMANDS`          | `models/commands.py`, seed migration                                       | Unit: gout/consult listed                                        |


**Sprint 1 status (2026-08-17):** A-1–A-11 done. Profile/allergy/gout slice plus FHIR JSONB on write, S3-compatible object store (URI + hash only), `POST /admin/migrate` domain upsert, Module 21 Postgres adapter, and `command_catalog` seed.




### Suggested first vertical slice (A)

Profile + allergies + gout flares only — prove adapter + RLS + migrate before cloning every tracker.

### Exit criteria

- [x] Staging/prod `DATABASE_URL` is Postgres; SQLite not used outside unit tests  
- [x] Alembic is the only schema path in CI for platform  
- [x] RLS negative tests pass on clinical + tracker tables  
- [x] `POST /commands/execute` with `profile` / `gout` / `allergy` persists in Postgres when `HEALTH_STORE=postgres`  
- [x] Pod restart does not lose those rows  
- [x] Local IDE JSON path still works (`HEALTH_STORE=json` or CLI-only)



### Risks


| Risk                            | Mitigation                                                                |
| ------------------------------- | ------------------------------------------------------------------------- |
| Tracker explosion (60 commands) | Slice: 3 domains first; generate tables from `data-example` schemas later |
| SQLite tests vs Postgres RLS    | RLS tests **must** run on Postgres in CI (service container)              |
| Dual-read split brain           | Time-box dual mode; A-9 flag default `postgres` in staging                |


---



## 5. Phase B — Identity and access



### Objectives

Enterprise SSO is primary auth. Authorization is a single PDP (RBAC + consent + purpose). Production CORS is explicit.

### Work items


| ID   | Task                                                                                                                       | Primary files                        | Tests                                                                       |
| ---- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | --------------------------------------------------------------------------- |
| B-1  | OIDC login (authorization code + PKCE for BFF; JWT bearer for API/MCP)                                                     | `auth/oidc.py`, `api/routes/auth.py` | Integration: mock IdP (e.g. testcontainers Keycloak or recorded well-known) |
| B-2  | Short-lived access JWT (15 min) + refresh or BFF session cookie                                                            | `auth/jwt.py`, session table         | Unit: expiry; integration: refresh rotation                                 |
| B-3  | Map IdP groups → roles (`patient`, `clinician`, `admin`, `auditor`, `tenant_admin`, `privacy_officer`)                     | `auth/roles.py`, `models/iam.py`     | Unit: group mapping                                                         |
| B-4  | MFA: document IdP requirement; reject tokens without `amr` containing `mfa` for privileged roles when `APP_ENV=production` | `auth/middleware.py`                 | Unit: clinician token without MFA → 401 in prod settings                    |
| B-5  | Coded PDP: `authorize(subject, action, resource, context)`                                                                 | `auth/policy.py`                     | Unit: matrix of allow/deny                                                  |
| B-6  | Consent + purpose on request context; LLM path refuses if `llm_processing` false                                           | `models/governance.py`, orchestrator | Unit + integration: 403 + audit `authz.denied`                              |
| B-7  | Break-glass role: time-boxed, extra audit, notify                                                                          | `auth/break_glass.py`                | Unit: expiry; audit event present                                           |
| B-8  | Production CORS allowlist; disable `allow_origins=["*"]` when not dev                                                      | `api/main.py`                        | Unit: settings-driven CORS                                                  |
| B-9  | MCP: token exchange / JWT only; no long-lived PAT in tool logs                                                             | `mcp/context.py`                     | Existing MCP auth tests + no-secret-in-logs                                 |
| B-10 | Optional SCIM stub (users/groups) — can slip to E if needed                                                                | `api/routes/scim.py`                 | Contract tests                                                              |
| B-11 | Disable password login when `APP_ENV` in staging/prod                                                                      | `api/routes/auth.py`                 | Unit: 404/403 on `/login` password in prod                                  |


**Sprint 2 status (2026-08-17):** B-1–B-11 done. OIDC uses a mockable client (Keycloak optional on Compose `infra`). SCIM is a list/501 stub. Dev keeps password login; staging/prod require OIDC.




### Exit criteria

- [x] Clinician can sign in via OIDC (staging IdP) and receive tenant-scoped JWT  
- [x] Privileged roles in prod settings require MFA claim  
- [x] PDP is the only authorization check on new routes (no new scattered `if role ==`)  
- [x] Wildcard CORS off in staging/prod config  
- [x] Password login off in staging/prod  
- [x] Cross-tenant API tests still pass  



### Risks


| Risk                    | Mitigation                                                    |
| ----------------------- | ------------------------------------------------------------- |
| IdP availability        | Dev keeps local JWT; staging uses Keycloak in Compose `infra` |
| Cookie vs JWT confusion | Document: browsers → BFF; MCP/API → Bearer                    |


---



## 6. Phase C — Observability and audit



### Objectives

Operational logs are structured and PHI-free. Compliance audit is durable, signed, hash-chained, and exportable.

### Work items


| ID   | Task                                                                          | Primary files                                                        | Tests                                                    |
| ---- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------- |
| C-1  | OpenTelemetry SDK: traces + metrics + JSON logs                               | `observability/otel.py`, `api/main.py` lifespan                      | Integration: span around `/commands/execute`             |
| C-2  | Correlation: `trace_id` / `request_id` on all responses                       | middleware                                                           | Unit: header present                                     |
| C-3  | PHI-free log formatter (deny names, emails, MRN, lab-like numbers in message) | `observability/log_filter.py`                                        | **Release negative tests** with planted PHI              |
| C-4  | Persist `audit_events` to Postgres (replace in-memory default)                | `audit/events.py`, `models/audit.py`                                 | Integration: event survives restart                      |
| C-5  | Hash chain: `prev_hash` + payload → `event_hash`; KMS or HMAC sign            | `audit/chain.py`                                                     | Unit: tamper detection                                   |
| C-6  | Append-only DB grants (no UPDATE/DELETE for app role)                         | migration                                                            | Integration: UPDATE fails                                |
| C-7  | Partition `audit_events` by month                                             | migration                                                            | Ops note + query still works                             |
| C-8  | Auditor API: filter by time, user, event_type, command; JSONL export          | `api/routes/admin.py`                                                | Integration: scope `audit` only                          |
| C-9  | Kafka/SIEM sink remains optional copy — Postgres is SoR                       | `audit/kafka_sink.py`                                                | Existing Kafka tests                                     |
| C-10 | Metrics: auth failures, RLS denials, anonymize failures, review-queue age     | `observability/metrics.py`                                           | Unit increment                                           |
| C-11 | Alert rules: audit-write failure (page), PHI-block spike, auth-fail spike     | `deploy/k8s/base/prometheus-rules.yaml`, `docs/runbooks/alerting.md` | Rule YAML valid                                          |
| C-12 | WORM archive job: monthly roll to object store (Object Lock when available)   | `jobs/audit_archive.py`                                              | Unit: mock store; skip if legal hold (flag stub until E) |




### Exit criteria

- [x] Default audit path is Postgres, not memory, when `AUDIT_USE_MEMORY=false`
- [x] Hash-chain verification utility passes on a sample stream
- [x] Planted PHI does not appear in captured application logs
- [x] Auditor can export JSONL for a date range
- [x] `/metrics` includes new counters; alert rules merged



### Risks


| Risk                      | Mitigation                                               |
| ------------------------- | -------------------------------------------------------- |
| Log volume                | Sample debug; never log bodies on clinical routes        |
| Chain breaks on partition | Chain per-tenant per-day or include partition seed event |


**Sprint 3 status (2026-08-17):** C-1–C-12 done. OTel traces + JSON PHI-free logs, `X-Request-ID` / `X-Trace-ID`, Postgres `audit_events` with HMAC hash chain (per tenant per day), append-only ORM + Postgres trigger, monthly `partition_month` column (native RANGE partition deferred), auditor JSONL export, Kafka remains optional copy, WORM archive stub skips on `AUDIT_LEGAL_HOLD`. Tests keep `AUDIT_USE_MEMORY=true`; Compose `core` and K8s use Postgres audit.


---



## 7. Phase D — PHI handling and flexible models



### Objectives

No external LLM call without anonymization + policy. Model choice is catalog + tenant policy, not a Python dict only.

### Work items


| ID   | Task                                                                                        | Primary files                                 | Tests                                                    |
| ---- | ------------------------------------------------------------------------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| D-1  | Presidio **on** by default when `APP_ENV` in staging/prod                                   | `anonymization/engine.py`, `core/config.py`   | Release: `tests/release/test_phi_safety.py`              |
| D-2  | Custom recognizers (MRN, accession, Indian phone variants as needed)                        | `anonymization/recognizers.py`                | Unit fixtures                                            |
| D-3  | Token map in Vault/KMS (tenant DEK); no in-memory-only in prod                              | `anonymization/vault_store.py`                | Existing vault tests + fail-closed                       |
| D-4  | Orchestrator: consent check → anonymize → **then** model policy                             | `services/command_orchestrator.py`            | Integration: fail anonymize → no HTTP to provider (mock) |
| D-5  | `model_catalog` table + seed (mock, anthropic, openai, google)                              | `models/models_catalog.py`, migration         | Unit                                                     |
| D-6  | `tenant_model_policies` (allowlist, residency, baa_required, budget, pin critical commands) | same                                          | Unit                                                     |
| D-7  | `ModelPolicyEngine.route(...)` replacing sole use of `ROUTING_TABLE`                        | `llm/policy.py`; keep router as default hints | Unit: BAA fail, residency fail, budget fail, fallback    |
| D-8  | `routing_decisions_log` (model, reason codes)                                               | `models/`, orchestrator                       | Integration                                              |
| D-9  | Admin APIs: list catalog, get/set tenant policy (admin scope)                               | `api/routes/admin.py` or `routes/models.py`   | Integration                                              |
| D-10 | BYOM stub: `vllm` provider + mTLS settings                                                  | `llm/providers.py`                            | Unit mock                                                |
| D-11 | Module 21 stays in-process; optional anonymized narrative overlay **off** by default        | `services/ai_service.py`                      | Unit: predict never calls LLM                            |
| D-12 | BAA registry table (replace docs-only for enforcement)                                      | `models/governance.py`, gate in policy        | Unit: unsigned + prod → deny                             |




### Exit criteria

- [x] Staging: Presidio on; anonymization failure blocks LLM (no provider call)
- [x] Tenant admin can pin `consult` to a catalog model and forbid non-BAA providers
- [x] Routing decision is audited (hash + model id + reason)
- [x] `/ai predict` still does not call an external LLM
- [x] Success criterion 3 and 6 from architecture §18 demonstrable in staging



### Risks


| Risk                            | Mitigation                                     |
| ------------------------------- | ---------------------------------------------- |
| Presidio latency                | Cache analyzer; timeout + fail-closed          |
| Catalog drift vs code fallbacks | Seed + “enabled” flag; tests for unknown model |


**Sprint 4 status (2026-08-17):** D-1–D-12 done. Presidio on by default in staging/prod (`presidio_is_enabled()`); custom MRN/accession/Indian-phone recognizers; in-memory token vault forbidden in staging/prod; orchestrator is consent → anonymize → `ModelPolicyEngine` → provider; `model_catalog` + `tenant_model_policies` + `routing_decisions_log` + `baa_records`; vLLM BYOM stub; Module 21 predict stays in-process (`AI_NARRATIVE_OVERLAY` off). `HealthLLMRouter.ROUTING_TABLE` remains hint-only.


---



## 8. Phase E — Privacy operations, HA, MDT workers



### Objectives

Demonstrate DSR, legal hold, backup/restore, and (optional) platform MDT closer to IDE `/consult`.

### Work items


| ID   | Task                                                                   | Primary files                                    | Tests                                                    |
| ---- | ---------------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------- |
| E-1  | `dsr_requests` workflow: access / erase / correct                      | `api/routes/privacy.py`, `jobs/dsr.py`           | Integration: erase removes rows + object prefix + tokens |
| E-2  | Completion certificate (no PHI)                                        | `jobs/dsr.py`                                    | Unit: certificate schema                                 |
| E-3  | Legal hold flag: skip purge/archive delete                             | `models/governance.py`, C-12 job                 | Unit                                                     |
| E-4  | Key rotation runbook **executed** in staging (JWT + tenant DEK)        | `docs/runbooks/secret-rotation.md`, ops log      | Drill checklist                                          |
| E-5  | HA Postgres (managed primary + replica) + encrypted PITR               | `deploy/k8s/`, `docs/runbooks/backup-restore.md` | Restore drill: CI identity dump/restore; live staging PITR operator-owned |
| E-6  | Rollback drill for API + MCP                                           | `mydocs/ops-log.md`                              | Checklist                                                |
| E-7  | NetworkPolicies default-deny; egress allowlist to LLM                  | `deploy/k8s/`                                    | Manifest review                                          |
| E-8  | Optional: specialist worker pool (queue + specialist markdown prompts) | `workers/specialist.py`                          | Integration: `/consult` returns merged sections          |
| E-9  | Optional SCIM if slipped from B-10                                     | `api/routes/scim.py`                             | Contract                                                 |
| E-10 | External HIPAA/SOC 2 engagement packet from evidence store             | `docs/compliance/`                               | Process, not code                                        |




### Exit criteria

- [x] Erasure demo: user gone from DB, objects, token vault; audit certificate issued  
- [x] Legal hold prevents purge  
- [x] Backup restore drill logged (CI identity dump/restore in `tests/unit/test_backup_restore.py`; runbook + checklist shipped; live staging PITR still operator-owned)  
- [x] Architecture §18 criteria 1–8 demonstrable (8 = SME markdown still works)  
- [x] E-8 optional: do not block HA/DSR if workers slip  

**Sprint 5 status (2026-08-17):** E-1–E-10 done. DSR access/erase/correct + PHI-free certificates; legal hold on erase and WORM archive; JWT dual-verify (`JWT_SECRET_PREVIOUS`); default-deny NetworkPolicies; specialist worker pool for `/consult`; SCIM lists tenant users (create remains 501); HA/PITR and rollback runbooks; HIPAA/SOC 2 engagement packet index. CI restore drill: `jobs/backup_restore.py` identity dump → fresh DB. Live staging PITR/rollback execution remains an operator drill (`mydocs/ops-log.md`).  

---



## 9. Mapping to architecture success criteria


| #   | Criterion                                      | Phase that proves it |
| --- | ---------------------------------------------- | -------------------- |
| 1   | SSO+MFA, tenant-only patients                  | B (+ A data)         |
| 2   | Writes in Postgres survive restart             | A                    |
| 3   | LLM blocked if anonymize or BAA/residency fail | D                    |
| 4   | Aggregator logs have no names/MRN/labs         | C                    |
| 5   | Signed hash-chained audit export               | C                    |
| 6   | Tenant pins `consult`, forbids non-BAA         | D                    |
| 7   | Erasure + certificate                          | E                    |
| 8   | SME markdown without platform rewrite          | All (gate)           |


---



## 10. Test strategy


| Layer       | Location             | Focus                                           |
| ----------- | -------------------- | ----------------------------------------------- |
| Unit        | `tests/unit/`        | Adapters, PDP, chain, policy engine, log filter |
| Integration | `tests/integration/` | API + Postgres service                          |
| Release     | `tests/release/`     | Tenant isolation, PHI safety, no-PHI-in-logs    |
| Eval        | `tests/eval/`        | Guardrail/model regression (unchanged intent)   |
| E2E         | `tests/e2e/`         | Login → command → audit row                     |
| Ops         | Runbooks             | Backup, rotation, rollback drills               |


CI: add a **Postgres service** job for A-4/A-5/C-4; SQLite may remain for fast unit tests that do not claim RLS.

---



## 11. Documentation updates per phase


| Phase | Docs to touch                                                                        |
| ----- | ------------------------------------------------------------------------------------ |
| A     | `local-development.md`, `data-structures.md` (DB mapping), `platform/README.md`      |
| B     | `consent-flow.md`, `compliance-controls.md`, auth section in `platform/README.md`    |
| C     | `slo.md`, `runbooks/alerting.md`, `compliance-controls.md` (audit integrity)         |
| D     | `baa-tracking.md`, `platform/README.md` (model catalog), `ui-mcp-integration.md`     |
| E     | `runbooks/backup-restore.md`, `compliance/soc2-evidence.md`, this plan’s exit checks |


Do **not** duplicate command specs in the user guide.

---



## 12. Team shape (indicative)


| Role               | A                   | B            | C              | D            | E         |
| ------------------ | ------------------- | ------------ | -------------- | ------------ | --------- |
| Backend            | Lead                | Lead         | Shared         | Lead         | Shared    |
| Security / privacy | Review RLS          | Lead IdP/PDP | Log PHI review | Presidio/BAA | DSR       |
| SRE                | Compose/CI Postgres | —            | OTel/alerts    | —            | HA/drills |
| SME                | Unblocked           | Unblocked    | Unblocked      | Unblocked    | Unblocked |


SMEs continue shipping markdown in parallel; platform squad owns A–E.

---



## 13. First sprint recommendation

If starting now, **Sprint 1 = A-1 + A-2 + A-3 (iam + audit + profile/allergy/gout only) + A-4 RLS on those tables**. That unblocks every later phase without boiling the ocean of 60 trackers.

---

*Implementation follows SYN-ARCH-ENT-001. Mark checkboxes in this file (or a project board cloned from the ID tables) as work completes. Do not skip A’s RLS tests to “move faster” into SSO.*