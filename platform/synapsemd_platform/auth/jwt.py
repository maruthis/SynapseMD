import bcrypt
from datetime import UTC, datetime, timedelta
from enum import Enum
from uuid import UUID

from jose import JWTError, jwt
from pydantic import BaseModel

from synapsemd_platform.core.config import get_settings

settings = get_settings()


class Role(str, Enum):
    PATIENT = "patient"
    CLINICIAN = "clinician"
    ADMIN = "admin"
    AUDITOR = "auditor"


ROLE_SCOPES: dict[Role, set[str]] = {
    Role.PATIENT: {"read:own", "write:own"},
    Role.CLINICIAN: {"read:own", "write:own", "read:org"},
    Role.ADMIN: {"read:own", "write:own", "read:org", "admin"},
    Role.AUDITOR: {"read:org", "audit"},
}


class TokenClaims(BaseModel):
    sub: UUID
    org: UUID
    roles: list[str]
    scope: list[str]
    exp: datetime | None = None


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
) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=expires_minutes or settings.jwt_expire_minutes)
    payload = {
        "sub": str(user_id),
        "org": str(tenant_id),
        "roles": roles,
        "scope": scopes or _scopes_for_roles(roles),
        "exp": expire,
        "iss": settings.oidc_issuer or "synapsemd-local",
        "aud": settings.oidc_audience,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> TokenClaims:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.oidc_audience,
            options={"verify_aud": bool(settings.oidc_audience)},
        )
    except JWTError as exc:
        raise ValueError("Invalid token") from exc

    return TokenClaims(
        sub=UUID(payload["sub"]),
        org=UUID(payload["org"]),
        roles=payload.get("roles", []),
        scope=payload.get("scope", []),
        exp=datetime.fromtimestamp(payload["exp"], tz=UTC) if "exp" in payload else None,
    )


def _scopes_for_roles(roles: list[str]) -> list[str]:
    scopes: set[str] = set()
    for role_name in roles:
        try:
            scopes.update(ROLE_SCOPES[Role(role_name)])
        except ValueError:
            continue
    return sorted(scopes)


def has_scope(claims: TokenClaims, required: str) -> bool:
    return required in claims.scope or "admin" in claims.roles


def has_role(claims: TokenClaims, *roles: str) -> bool:
    return any(role in claims.roles for role in roles)
