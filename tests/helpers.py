from uuid import uuid4

from synapsemd_platform.auth.jwt import create_access_token


def make_token(*, user_id=None, tenant_id=None, roles=None, scopes=None) -> str:
    return create_access_token(
        user_id=user_id or uuid4(),
        tenant_id=tenant_id or uuid4(),
        roles=roles or ["patient"],
        scopes=scopes or ["read:own", "write:own"],
    )
