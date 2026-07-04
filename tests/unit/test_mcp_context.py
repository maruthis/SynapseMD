"""Extended MCP auth context tests."""

from uuid import uuid4

import pytest

from synapsemd_platform.auth.jwt import create_access_token
from synapsemd_platform.mcp.context import McpAuthError, resolve_auth_context


def test_resolve_auth_context_tenant_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    other_tenant = uuid4()
    token = create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=["patient"],
        scopes=["read:own"],
    )
    monkeypatch.setenv("SYNAPSEMD_ACCESS_TOKEN", token)
    monkeypatch.setenv("SYNAPSEMD_TENANT_ID", str(other_tenant))
    with pytest.raises(McpAuthError, match="does not match"):
        resolve_auth_context()


def test_resolve_auth_context_with_matching_tenant_override(monkeypatch: pytest.MonkeyPatch) -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    token = create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )
    monkeypatch.setenv("SYNAPSEMD_ACCESS_TOKEN", token)
    monkeypatch.setenv("SYNAPSEMD_TENANT_ID", str(tenant_id))
    ctx = resolve_auth_context()
    assert ctx.tenant_id == tenant_id
    assert ctx.user_id == user_id
