"""Coverage for all MCP dispatch tool branches."""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from synapsemd_platform.mcp.dispatch import dispatch_tool
from synapsemd_platform.mcp.schemas import McpAuthContext


@pytest.fixture
def ctx() -> McpAuthContext:
    return McpAuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient", "auditor"],
        scopes=["read:own", "write:own", "audit"],
    )


@pytest.mark.asyncio
async def test_dispatch_get_profile_summary(ctx: McpAuthContext) -> None:
    with patch(
        "synapsemd_platform.mcp.tools.get_profile_summary",
        AsyncMock(return_value=type("R", (), {"model_dump": lambda self: {"patient_id": "p1"}})()),
    ):
        result = await dispatch_tool("get_profile_summary", ctx, {})
    assert result["patient_id"] == "p1"


@pytest.mark.asyncio
async def test_dispatch_query_fhir_records(ctx: McpAuthContext) -> None:
    with patch(
        "synapsemd_platform.mcp.tools.query_fhir_records",
        AsyncMock(return_value=type("R", (), {"model_dump": lambda self: {"count": 2}})()),
    ):
        result = await dispatch_tool("query_fhir_records", ctx, {"resource_type": "Patient"})
    assert result["count"] == 2


@pytest.mark.asyncio
async def test_dispatch_search_clinical_knowledge(ctx: McpAuthContext) -> None:
    with patch(
        "synapsemd_platform.mcp.tools.search_clinical_knowledge",
        AsyncMock(return_value=type("R", (), {"model_dump": lambda self: {"count": 1}})()),
    ):
        result = await dispatch_tool("search_clinical_knowledge", ctx, {"query": "diabetes"})
    assert result["count"] == 1


@pytest.mark.asyncio
async def test_dispatch_get_audit_summary(ctx: McpAuthContext) -> None:
    with patch(
        "synapsemd_platform.mcp.tools.get_audit_summary",
        AsyncMock(return_value=type("R", (), {"model_dump": lambda self: {"count": 0}})()),
    ):
        result = await dispatch_tool("get_audit_summary", ctx, {"limit": 10})
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_dispatch_execute_command(ctx: McpAuthContext) -> None:
    with patch(
        "synapsemd_platform.mcp.tools.execute_command",
        AsyncMock(return_value=type("R", (), {"model_dump": lambda self: {"command": "goal"}})()),
    ):
        result = await dispatch_tool("execute_command", ctx, {"command": "goal"})
    assert result["command"] == "goal"
