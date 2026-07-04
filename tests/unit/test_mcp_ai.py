from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from synapsemd_platform.mcp.context import McpAuthError
from synapsemd_platform.mcp.dispatch import MCP_TOOL_NAMES, dispatch_tool
from synapsemd_platform.mcp.schemas import AiChatInput, AiPredictInput, McpAuthContext


@pytest.fixture
def auth_ctx() -> McpAuthContext:
    return McpAuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )


@pytest.fixture
def read_only_ctx() -> McpAuthContext:
    return McpAuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient"],
        scopes=["read:own"],
    )


@pytest.mark.asyncio
async def test_mcp_tool_names_include_ai() -> None:
    assert "ai_status" in MCP_TOOL_NAMES
    assert "ai_predict" in MCP_TOOL_NAMES
    assert len(MCP_TOOL_NAMES) == 11


@pytest.mark.asyncio
async def test_dispatch_ai_status(auth_ctx: McpAuthContext) -> None:
    mock_status = AsyncMock(
        return_value={"enabled": True, "disclaimer": "Not medical advice"}
    )
    with patch("synapsemd_platform.mcp.tools._ai_service.status", mock_status):
        result = await dispatch_tool("ai_status", auth_ctx, {})
    assert result["action"] == "status"
    assert result["result"]["enabled"] is True
    mock_status.assert_awaited_once()


@pytest.mark.asyncio
async def test_dispatch_ai_predict(auth_ctx: McpAuthContext) -> None:
    mock_predict = AsyncMock(
        return_value={"risk_type": "hypertension", "risk_level": "moderate"}
    )
    with patch("synapsemd_platform.mcp.tools._ai_service.predict", mock_predict):
        result = await dispatch_tool("ai_predict", auth_ctx, {"risk_type": "hypertension"})
    assert result["action"] == "predict"
    assert result["result"]["risk_type"] == "hypertension"


@pytest.mark.asyncio
async def test_dispatch_ai_analyze(auth_ctx: McpAuthContext) -> None:
    mock_analyze = AsyncMock(return_value={"predictions": [], "disclaimer": "test"})
    with patch("synapsemd_platform.mcp.tools._ai_service.analyze", mock_analyze):
        result = await dispatch_tool("ai_analyze", auth_ctx, {"time_range": "last_quarter"})
    assert result["action"] == "analyze"
    assert "predictions" in result["result"]


@pytest.mark.asyncio
async def test_dispatch_ai_chat(auth_ctx: McpAuthContext) -> None:
    mock_chat = AsyncMock(return_value={"response": "Sleep looks stable", "disclaimer": "test"})
    with patch("synapsemd_platform.mcp.tools._ai_service.chat", mock_chat):
        result = await dispatch_tool("ai_chat", auth_ctx, {"query": "How is my sleep?"})
    assert result["action"] == "chat"
    assert result["result"]["response"]


@pytest.mark.asyncio
async def test_dispatch_ai_report(auth_ctx: McpAuthContext) -> None:
    mock_report = AsyncMock(
        return_value={"report_type": "comprehensive", "summary": "Overall stable"}
    )
    with patch("synapsemd_platform.mcp.tools._ai_service.report", mock_report):
        result = await dispatch_tool(
            "ai_report",
            auth_ctx,
            {"report_type": "comprehensive", "time_range": "last_quarter"},
        )
    assert result["action"] == "report"
    assert result["result"]["report_type"] == "comprehensive"


@pytest.mark.asyncio
async def test_dispatch_ai_predict_requires_write_scope(read_only_ctx: McpAuthContext) -> None:
    with pytest.raises(McpAuthError, match="Missing scope"):
        await dispatch_tool("ai_predict", read_only_ctx, {"risk_type": "diabetes"})


@pytest.mark.asyncio
async def test_dispatch_unknown_tool(auth_ctx: McpAuthContext) -> None:
    with pytest.raises(ValueError, match="Unknown tool"):
        await dispatch_tool("not_a_tool", auth_ctx, {})


def test_ai_input_validation() -> None:
    with pytest.raises(Exception):
        AiChatInput(query="")
    assert AiPredictInput().risk_type == "hypertension"
