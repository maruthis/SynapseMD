"""In-process policy decision point (RBAC + consent + purpose)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from synapsemd_platform.auth.roles import Role
from synapsemd_platform.core.context import RequestContext

LLM_COMMANDS: frozenset[str] = frozenset(
    {
        "goal",
        "consult",
        "specialist",
        "nutrition",
        "fitness",
        "sleep",
        "mental-health",
        "interaction",
        "query",
        "health-trend-analyzer",
    }
)

HEALTH_COMMANDS: frozenset[str] = frozenset({"profile", "allergy", "gout"})


class AuthzDenied(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class Subject:
    user_id: UUID
    tenant_id: UUID
    roles: tuple[str, ...]
    scopes: tuple[str, ...]
    amr: tuple[str, ...] = ()
    break_glass: bool = False

    @classmethod
    def from_context(cls, ctx: RequestContext) -> Subject:
        return cls(
            user_id=ctx.user_id,
            tenant_id=ctx.tenant_id,
            roles=ctx.roles,
            scopes=ctx.scopes,
            amr=ctx.amr,
            break_glass="break_glass" in ctx.roles,
        )


@dataclass(frozen=True)
class Resource:
    type: str
    id: str | None = None
    tenant_id: UUID | None = None


@dataclass(frozen=True)
class AuthzContext:
    purpose: str = "treatment"
    llm_processing: bool = True
    app_env: str = "development"


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def authorize(subject: Subject, action: str, resource: Resource, context: AuthzContext) -> Decision:
    if resource.tenant_id is not None and resource.tenant_id != subject.tenant_id:
        if not subject.break_glass:
            return Decision(False, "cross_tenant_denied")

    if resource.type == "command" and action == "execute":
        command = resource.id or ""
        if command in LLM_COMMANDS and not context.llm_processing:
            return Decision(False, "llm_processing_consent_required")
        if subject.break_glass:
            return Decision(True, "allow")
        if "write:own" in subject.scopes or "read:own" in subject.scopes or "admin" in subject.roles:
            return Decision(True, "allow")
        return Decision(False, "missing_scope")

    if resource.type == "admin":
        if "admin" in subject.scopes or "admin" in subject.roles or Role.TENANT_ADMIN.value in subject.roles:
            return Decision(True, "allow")
        return Decision(False, "admin_required")

    if resource.type == "audit":
        if "audit" in subject.scopes or "admin" in subject.roles:
            return Decision(True, "allow")
        return Decision(False, "audit_required")

    if resource.type == "break_glass" and action == "activate":
        if any(role in subject.roles for role in (Role.CLINICIAN.value, Role.ADMIN.value, Role.TENANT_ADMIN.value)):
            return Decision(True, "allow")
        return Decision(False, "break_glass_forbidden")

    if resource.type == "scim":
        if "admin" in subject.scopes or Role.TENANT_ADMIN.value in subject.roles:
            return Decision(True, "allow")
        return Decision(False, "scim_forbidden")

    if resource.type == "privacy":
        if (
            "privacy" in subject.scopes
            or "admin" in subject.scopes
            or Role.PRIVACY_OFFICER.value in subject.roles
            or "admin" in subject.roles
            or Role.TENANT_ADMIN.value in subject.roles
        ):
            return Decision(True, "allow")
        return Decision(False, "privacy_required")

    if resource.type == "consent" and action in {"read", "write"}:
        if "write:own" in subject.scopes or "read:own" in subject.scopes:
            return Decision(True, "allow")
        return Decision(False, "missing_scope")

    return Decision(False, "no_matching_policy")
