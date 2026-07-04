"""Central MCP tool dispatch used by stdio server and OpenAPI bridge."""

from __future__ import annotations

from typing import Any

from synapsemd_platform.mcp import tools as mcp_tools
from synapsemd_platform.mcp.schemas import (
    AiAnalyzeInput,
    AiChatInput,
    AiPredictInput,
    AiReportInput,
    ExecuteCommandInput,
    McpAuthContext,
    QueryFhirInput,
    SearchKnowledgeInput,
)

MCP_TOOL_NAMES: list[str] = [
    "list_commands",
    "execute_command",
    "get_profile_summary",
    "query_fhir_records",
    "search_clinical_knowledge",
    "get_audit_summary",
    "ai_status",
    "ai_analyze",
    "ai_predict",
    "ai_chat",
    "ai_report",
]


async def dispatch_tool(
    name: str,
    ctx: McpAuthContext,
    arguments: dict[str, Any] | None = None,
) -> dict[str, Any]:
    args = arguments or {}

    if name == "list_commands":
        return (await mcp_tools.list_commands(ctx)).model_dump()
    if name == "execute_command":
        return (await mcp_tools.execute_command(ctx, ExecuteCommandInput(**args))).model_dump()
    if name == "get_profile_summary":
        return (await mcp_tools.get_profile_summary(ctx)).model_dump()
    if name == "query_fhir_records":
        return (await mcp_tools.query_fhir_records(ctx, QueryFhirInput(**args))).model_dump()
    if name == "search_clinical_knowledge":
        return (await mcp_tools.search_clinical_knowledge(ctx, SearchKnowledgeInput(**args))).model_dump()
    if name == "get_audit_summary":
        return (await mcp_tools.get_audit_summary(ctx, limit=int(args.get("limit", 50)))).model_dump()
    if name == "ai_status":
        return (await mcp_tools.ai_status(ctx)).model_dump()
    if name == "ai_analyze":
        return (await mcp_tools.ai_analyze(ctx, AiAnalyzeInput(**args))).model_dump()
    if name == "ai_predict":
        return (await mcp_tools.ai_predict(ctx, AiPredictInput(**args))).model_dump()
    if name == "ai_chat":
        return (await mcp_tools.ai_chat(ctx, AiChatInput(**args))).model_dump()
    if name == "ai_report":
        return (await mcp_tools.ai_report(ctx, AiReportInput(**args))).model_dump()

    raise ValueError(f"Unknown tool: {name}")
