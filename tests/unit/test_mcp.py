import os
from uuid import uuid4

import pytest

from synapsemd_platform.auth.jwt import create_access_token
from synapsemd_platform.mcp.context import McpAuthError, resolve_auth_context
from synapsemd_platform.mcp.schemas import ExecuteCommandInput
from synapsemd_platform.mcp import tools as mcp_tools
from synapsemd_platform.mcp.schemas import McpAuthContext


@pytest.fixture
def auth_ctx() -> McpAuthContext:
    user_id = uuid4()
    tenant_id = uuid4()
    token = create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )
    os.environ["SYNAPSEMD_ACCESS_TOKEN"] = token
    return McpAuthContext(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )


def test_resolve_auth_context_missing_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SYNAPSEMD_ACCESS_TOKEN", raising=False)
    with pytest.raises(McpAuthError):
        resolve_auth_context()


@pytest.mark.asyncio
async def test_mcp_list_commands(auth_ctx: McpAuthContext) -> None:
    result = await mcp_tools.list_commands(auth_ctx)
    assert result.count > 0
    assert "goal" in result.commands
    assert "ai" in result.commands


@pytest.mark.asyncio
async def test_mcp_execute_command(auth_ctx: McpAuthContext) -> None:
    body = ExecuteCommandInput(command="goal", context_text="Lose 5kg safely")
    result = await mcp_tools.execute_command(auth_ctx, body)
    assert result.command == "goal"
    assert result.blocked is False


@pytest.mark.asyncio
async def test_mcp_audit_requires_scope(auth_ctx: McpAuthContext) -> None:
    with pytest.raises(McpAuthError, match="Missing scope"):
        await mcp_tools.get_audit_summary(auth_ctx)


def test_resolve_auth_context_success(auth_ctx: McpAuthContext) -> None:
    import os

    token = os.environ.get("SYNAPSEMD_ACCESS_TOKEN", "")
    assert token
    ctx = resolve_auth_context()
    assert ctx.user_id == auth_ctx.user_id
    assert ctx.tenant_id == auth_ctx.tenant_id
