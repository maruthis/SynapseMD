from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from jose import jwt

from synapsemd_platform.auth.jwt import (
    Role,
    TokenClaims,
    create_access_token,
    decode_access_token,
    has_role,
    has_scope,
    hash_password,
    verify_password,
    _scopes_for_roles,
)
from synapsemd_platform.core.config import get_settings


def test_hash_and_verify_password() -> None:
    hashed = hash_password("securepass1")
    assert verify_password("securepass1", hashed)
    assert not verify_password("wrong", hashed)


def test_create_and_decode_token() -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    token = create_access_token(user_id=user_id, tenant_id=tenant_id, roles=["patient"])
    claims = decode_access_token(token)
    assert claims.sub == user_id
    assert claims.org == tenant_id
    assert "patient" in claims.roles


def test_decode_invalid_token() -> None:
    with pytest.raises(ValueError, match="Invalid token"):
        decode_access_token("not-a-valid-token")


def test_decode_expired_token() -> None:
    settings = get_settings()
    user_id = uuid4()
    tenant_id = uuid4()
    expire = datetime.now(UTC) - timedelta(minutes=1)
    payload = {
        "sub": str(user_id),
        "org": str(tenant_id),
        "roles": ["patient"],
        "scope": ["read:own"],
        "exp": expire,
        "aud": settings.oidc_audience,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    with pytest.raises(ValueError):
        decode_access_token(token)


def test_scopes_for_roles_all_roles() -> None:
    for role in Role:
        scopes = _scopes_for_roles([role.value])
        assert len(scopes) > 0


def test_scopes_for_unknown_role() -> None:
    assert _scopes_for_roles(["unknown-role"]) == []


def test_has_scope_and_admin_bypass() -> None:
    claims = TokenClaims(sub=uuid4(), org=uuid4(), roles=["admin"], scope=[])
    assert has_scope(claims, "admin")
    patient = TokenClaims(sub=uuid4(), org=uuid4(), roles=["patient"], scope=["read:own"])
    assert has_scope(patient, "read:own")
    assert not has_scope(patient, "admin")


def test_has_role() -> None:
    claims = TokenClaims(sub=uuid4(), org=uuid4(), roles=["clinician"], scope=[])
    assert has_role(claims, "clinician")
    assert not has_role(claims, "admin")
