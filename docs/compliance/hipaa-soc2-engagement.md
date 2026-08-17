# HIPAA / SOC 2 Engagement Packet

**Document ID:** SYN-COMP-ENG-001  
**Status:** Packet index — schedule dates with counsel; do not treat as an executed audit  
**Date:** 2026-08-17

This packet is the evidence index for an external HIPAA or SOC 2 engagement. Store working papers in the org evidence repository (not git). Paths below are the in-repo control descriptions.

## Packet contents

| Tab | Artifact | Location |
|-----|----------|----------|
| 1 | Architecture and trust boundary | [enterprise-platform-architecture.md](../enterprise-platform-architecture.md) |
| 2 | Control mapping (HIPAA / GDPR / SOC 2) | [compliance-controls.md](../compliance-controls.md) |
| 3 | SOC 2 evidence process | [soc2-evidence.md](soc2-evidence.md) |
| 4 | Consent and purpose | [consent-flow.md](../consent-flow.md) |
| 5 | PHI handling / Presidio | [runbooks/phi-handling.md](../runbooks/phi-handling.md) |
| 6 | BAA registry | [baa-tracking.md](../baa-tracking.md) |
| 7 | Backup / PITR / HA | [runbooks/backup-restore.md](../runbooks/backup-restore.md) |
| 7a | Object store (URI + hash, no blob in DB) | [data-structures.md](../data-structures.md) § Platform SoR mapping |
| 8 | Secret / DEK rotation | [runbooks/secret-rotation.md](../runbooks/secret-rotation.md) |
| 9 | Incident response | [runbooks/incident-response.md](../runbooks/incident-response.md) |
| 10 | Release gates | [release-gates.md](../release-gates.md) |
| 11 | DSR / legal hold | `POST /privacy/dsr`, `POST /privacy/legal-hold` |
| 12 | NetworkPolicies | `deploy/k8s/base/network-policies.yaml` |
| 13 | Automated tests | `tests/release/` (tenant isolation, PHI safety, RLS) |

## External engagement

| Milestone | Owner | Target date | Status |
|-----------|-------|-------------|--------|
| Readiness assessment | Security / privacy | (schedule) | Packet ready |
| HIPAA risk analysis | Counsel + security | (schedule) | Planned |
| SOC 2 Type I | External auditor | (schedule) | Planned |
| SOC 2 Type II | External auditor | (schedule) | Planned |

Update dates in [soc2-evidence.md](soc2-evidence.md) when the engagement letter is signed.
