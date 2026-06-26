from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from synapsemd_platform.auth.jwt import TokenClaims, decode_access_token, has_scope
from synapsemd_platform.core.context import RequestContext, set_request_context

security = HTTPBearer(auto_error=False)


async def get_current_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> TokenClaims:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        return decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


async def get_request_ctx(claims: TokenClaims = Depends(get_current_claims)) -> RequestContext:
    ctx = RequestContext(
        user_id=claims.sub,
        tenant_id=claims.org,
        roles=tuple(claims.roles),
        scopes=tuple(claims.scope),
    )
    set_request_context(ctx)
    return ctx


def require_scope(scope: str):
    async def _checker(claims: TokenClaims = Depends(get_current_claims)) -> TokenClaims:
        if not has_scope(claims, scope):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing scope: {scope}")
        return claims

    return _checker
