import json
from unittest.mock import AsyncMock, patch

import pytest

from synapsemd_platform.mcp.server import _dispatch, list_tools


@pytest.mark.asyncio
async def test_mcp_list_tools() -> None:
    tools = await list_tools()
    names = {t.name for t in tools}
    assert "execute_command" in names
    assert "list_commands" in names
    assert "ai_status" in names
    assert "ai_predict" in names
    assert len(names) == 11


def test_create_sse_app_exposes_health_and_sse_routes() -> None:
    from synapsemd_platform.mcp.server import create_sse_app

    app = create_sse_app()
    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/health" in paths
    assert "/sse" in paths


@pytest.mark.asyncio
async def test_mcp_dispatch_list_commands_includes_ai(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.mcp.schemas import McpAuthContext
    from uuid import uuid4

    ctx = McpAuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )
    monkeypatch.setattr("synapsemd_platform.mcp.server.resolve_auth_context", lambda: ctx)
    result = await _dispatch("list_commands", {})
    assert "ai" in result["commands"]
