import os
import re
from uuid import UUID

from synapsemd_platform.auth.jwt import decode_access_token, has_scope
from synapsemd_platform.mcp.schemas import McpAuthContext

_JWT_RE = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


class McpAuthError(Exception):
    pass


def redact_secrets(text: str) -> str:
    return _JWT_RE.sub("[REDACTED]", text)


def resolve_auth_context() -> McpAuthContext:
    token = os.environ.get("SYNAPSEMD_ACCESS_TOKEN", "").strip()
    if not token:
        raise McpAuthError("SYNAPSEMD_ACCESS_TOKEN is required")

    claims = decode_access_token(token)
    tenant_override = os.environ.get("SYNAPSEMD_TENANT_ID", "").strip()
    tenant_id = UUID(tenant_override) if tenant_override else claims.org

    if tenant_id != claims.org:
        raise McpAuthError("SYNAPSEMD_TENANT_ID does not match token tenant")

    return McpAuthContext(
        user_id=claims.sub,
        tenant_id=tenant_id,
        roles=list(claims.roles),
        scopes=list(claims.scope),
        llm_processing=claims.llm_processing,
        purpose=claims.purpose,
    )


def require_scope(ctx: McpAuthContext, scope: str) -> None:
    from synapsemd_platform.auth.jwt import TokenClaims

    claims = TokenClaims(
        sub=ctx.user_id,
        org=ctx.tenant_id,
        roles=ctx.roles,
        scope=ctx.scopes,
    )
    if not has_scope(claims, scope):
        raise McpAuthError(f"Missing scope: {scope}")
