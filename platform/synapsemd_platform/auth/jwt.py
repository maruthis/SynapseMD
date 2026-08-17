from datetime import UTC, datetime, timedelta
from uuid import UUID

import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel, Field

from synapsemd_platform.auth.roles import ROLE_SCOPES, Role, scopes_for_roles
from synapsemd_platform.core.config import get_settings

__all__ = [
    "Role",
    "ROLE_SCOPES",
    "TokenClaims",
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "has_scope",
    "has_role",
    "scopes_for_roles",
    "_scopes_for_roles",
]


class TokenClaims(BaseModel):
    sub: UUID
    org: UUID
    roles: list[str]
    scope: list[str]
    exp: datetime | None = None
    amr: list[str] = Field(default_factory=list)
    purpose: str = "treatment"
    llm_processing: bool = True
    token_use: str = "access"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(
    *,
    user_id: UUID,
    tenant_id: UUID,
    roles: list[str],
    scopes: list[str] | None = None,
    expires_minutes: int | None = None,
    amr: list[str] | None = None,
    purpose: str = "treatment",
    llm_processing: bool = True,
) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=expires_minutes or settings.jwt_expire_minutes)
    payload = {
        "sub": str(user_id),
        "org": str(tenant_id),
        "roles": roles,
        "scope": scopes or scopes_for_roles(roles),
        "exp": expire,
        "iss": settings.oidc_issuer or "synapsemd-local",
        "aud": settings.oidc_audience,
        "amr": amr or ["pwd"],
        "purpose": purpose,
        "llm_processing": llm_processing,
        "token_use": "access",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> TokenClaims:
    settings = get_settings()
    secrets = [settings.jwt_secret]
    if settings.jwt_secret_previous:
        secrets.append(settings.jwt_secret_previous)
    payload = None
    last_error: Exception | None = None
    for secret in secrets:
        try:
            payload = jwt.decode(
                token,
                secret,
                algorithms=[settings.jwt_algorithm],
                audience=settings.oidc_audience,
                options={"verify_aud": bool(settings.oidc_audience)},
            )
            break
        except JWTError as exc:
            last_error = exc
    if payload is None:
        raise ValueError("Invalid token") from last_error

    if payload.get("token_use", "access") != "access":
        raise ValueError("Invalid token")

    return TokenClaims(
        sub=UUID(payload["sub"]),
        org=UUID(payload["org"]),
        roles=payload.get("roles", []),
        scope=payload.get("scope", []),
        exp=datetime.fromtimestamp(payload["exp"], tz=UTC) if "exp" in payload else None,
        amr=list(payload.get("amr") or []),
        purpose=str(payload.get("purpose") or "treatment"),
        llm_processing=bool(payload.get("llm_processing", True)),
        token_use=str(payload.get("token_use") or "access"),
    )


def _scopes_for_roles(roles: list[str]) -> list[str]:
    return scopes_for_roles(roles)


def has_scope(claims: TokenClaims, required: str) -> bool:
    return required in claims.scope or "admin" in claims.roles or "tenant_admin" in claims.roles


def has_role(claims: TokenClaims, *roles: str) -> bool:
    return any(role in claims.roles for role in roles)
