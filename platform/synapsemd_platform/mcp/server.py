import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from synapsemd_platform.mcp.context import McpAuthError, resolve_auth_context
from synapsemd_platform.mcp.dispatch import MCP_TOOL_NAMES, dispatch_tool

server = Server("synapsemd")


@server.list_tools()
async def list_tools() -> list[Tool]:
    schemas: dict[str, dict[str, Any]] = {
        "list_commands": {"type": "object", "properties": {}, "required": []},
        "execute_command": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "context_text": {"type": "string"},
                "payload": {"type": "object"},
            },
            "required": ["command"],
        },
        "get_profile_summary": {"type": "object", "properties": {}, "required": []},
        "query_fhir_records": {
            "type": "object",
            "properties": {
                "resource_type": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100},
            },
            "required": [],
        },
        "search_clinical_knowledge": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
                "include_org_intelligence": {"type": "boolean"},
            },
            "required": ["query"],
        },
        "get_audit_summary": {
            "type": "object",
            "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 200}},
            "required": [],
        },
        "ai_status": {"type": "object", "properties": {}, "required": []},
        "ai_analyze": {
            "type": "object",
            "properties": {"time_range": {"type": "string"}},
            "required": [],
        },
        "ai_predict": {
            "type": "object",
            "properties": {"risk_type": {"type": "string"}},
            "required": [],
        },
        "ai_chat": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        "ai_report": {
            "type": "object",
            "properties": {
                "report_type": {"type": "string"},
                "time_range": {"type": "string"},
            },
            "required": [],
        },
    }
    descriptions: dict[str, str] = {
        "list_commands": "List available SynapseMD health commands",
        "execute_command": "Execute a health command through the PHI-safe orchestrator",
        "get_profile_summary": "Get FHIR patient profile summary for the authenticated user",
        "query_fhir_records": "Query tenant-scoped FHIR resources for the authenticated user",
        "search_clinical_knowledge": "Search clinical knowledge base and optional org intelligence",
        "get_audit_summary": "Get recent audit events for the tenant (auditor scope required)",
        "ai_status": "Get Module 21 AI feature status for the authenticated user",
        "ai_analyze": "Run comprehensive AI health analysis with risk predictions",
        "ai_predict": "Predict a specific health risk (hypertension, diabetes, cardiovascular, etc.)",
        "ai_chat": "Ask a natural-language health question with PHI-safe processing",
        "ai_report": "Generate an AI health report summary",
    }
    return [
        Tool(name=name, description=descriptions[name], inputSchema=schemas[name])
        for name in MCP_TOOL_NAMES
    ]


async def _dispatch(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    ctx = resolve_auth_context()
    return await dispatch_tool(name, ctx, arguments)


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    args = arguments or {}
    try:
        result = await _dispatch(name, args)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except McpAuthError as exc:
        return [TextContent(type="text", text=json.dumps({"error": str(exc)}))]
    except Exception as exc:
        return [TextContent(type="text", text=json.dumps({"error": str(exc)}))]


async def run_stdio() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    asyncio.run(run_stdio())


if __name__ == "__main__":
    main()
