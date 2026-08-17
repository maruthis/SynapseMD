from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from synapsemd_platform.auth.jwt import TokenClaims, decode_access_token, has_scope
from synapsemd_platform.auth.roles import PRIVILEGED_ROLES
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.context import RequestContext, set_request_context
from synapsemd_platform.observability.metrics import AUTH_FAILURE_COUNT

security = HTTPBearer(auto_error=False)


def _enforce_mfa(claims: TokenClaims) -> None:
    settings = get_settings()
    if not settings.mfa_required_for_privileged():
        return
    if not (PRIVILEGED_ROLES & set(claims.roles)):
        return
    if "mfa" not in {item.lower() for item in claims.amr}:
        AUTH_FAILURE_COUNT.labels(reason="mfa_required").inc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="MFA required for privileged roles",
        )


async def get_current_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> TokenClaims:
    if credentials is None or credentials.scheme.lower() != "bearer":
        AUTH_FAILURE_COUNT.labels(reason="missing_bearer").inc()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        claims = decode_access_token(credentials.credentials)
    except ValueError as exc:
        AUTH_FAILURE_COUNT.labels(reason="invalid_token").inc()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    _enforce_mfa(claims)
    return claims


async def get_request_ctx(claims: TokenClaims = Depends(get_current_claims)) -> RequestContext:
    ctx = RequestContext(
        user_id=claims.sub,
        tenant_id=claims.org,
        roles=tuple(claims.roles),
        scopes=tuple(claims.scope),
        amr=tuple(claims.amr),
        purpose=claims.purpose,
        llm_processing=claims.llm_processing,
    )
    set_request_context(ctx)
    return ctx


def require_scope(scope: str):
    async def _checker(claims: TokenClaims = Depends(get_current_claims)) -> TokenClaims:
        if not has_scope(claims, scope):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing scope: {scope}")
        return claims

    return _checker
