"""RBAC roles, scopes, and IdP group mapping (Phase B)."""

from enum import Enum


class Role(str, Enum):
    PATIENT = "patient"
    CLINICIAN = "clinician"
    ADMIN = "admin"
    AUDITOR = "auditor"
    TENANT_ADMIN = "tenant_admin"
    PRIVACY_OFFICER = "privacy_officer"
    BREAK_GLASS = "break_glass"


ROLE_SCOPES: dict[Role, set[str]] = {
    Role.PATIENT: {"read:own", "write:own"},
    Role.CLINICIAN: {"read:own", "write:own", "read:org"},
    Role.ADMIN: {"read:own", "write:own", "read:org", "admin"},
    Role.AUDITOR: {"read:org", "audit"},
    Role.TENANT_ADMIN: {"read:own", "write:own", "read:org", "admin"},
    Role.PRIVACY_OFFICER: {"read:org", "audit", "privacy"},
    Role.BREAK_GLASS: {"read:org", "break_glass"},
}

PRIVILEGED_ROLES: frozenset[str] = frozenset(
    {
        Role.CLINICIAN.value,
        Role.ADMIN.value,
        Role.AUDITOR.value,
        Role.TENANT_ADMIN.value,
        Role.PRIVACY_OFFICER.value,
        Role.BREAK_GLASS.value,
    }
)

IDP_GROUP_ROLE_MAP: dict[str, Role] = {
    "synapsemd-patients": Role.PATIENT,
    "synapsemd-clinicians": Role.CLINICIAN,
    "synapsemd-admins": Role.ADMIN,
    "synapsemd-auditors": Role.AUDITOR,
    "synapsemd-tenant-admins": Role.TENANT_ADMIN,
    "synapsemd-privacy": Role.PRIVACY_OFFICER,
    "patient": Role.PATIENT,
    "clinician": Role.CLINICIAN,
    "admin": Role.ADMIN,
    "auditor": Role.AUDITOR,
    "tenant_admin": Role.TENANT_ADMIN,
    "privacy_officer": Role.PRIVACY_OFFICER,
}


def scopes_for_roles(roles: list[str]) -> list[str]:
    scopes: set[str] = set()
    for role_name in roles:
        try:
            scopes.update(ROLE_SCOPES[Role(role_name)])
        except ValueError:
            continue
    return sorted(scopes)


def map_idp_groups_to_roles(groups: list[str] | None, *, default: Role = Role.PATIENT) -> list[str]:
    """Map IdP group / role claim values to SynapseMD roles."""
    mapped: list[str] = []
    seen: set[str] = set()
    for raw in groups or []:
        key = raw.strip().lower().rsplit("/", 1)[-1]
        role = IDP_GROUP_ROLE_MAP.get(key) or IDP_GROUP_ROLE_MAP.get(raw.strip())
        if role is None:
            continue
        if role.value not in seen:
            seen.add(role.value)
            mapped.append(role.value)
    if not mapped:
        return [default.value]
    return mapped
