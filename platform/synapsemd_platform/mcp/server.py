import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from synapsemd_platform.mcp.context import McpAuthError, resolve_auth_context
from synapsemd_platform.mcp.schemas import ExecuteCommandInput, QueryFhirInput, SearchKnowledgeInput
from synapsemd_platform.mcp import tools as mcp_tools

server = Server("synapsemd")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_commands",
            description="List available SynapseMD health commands",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="execute_command",
            description="Execute a health command through the PHI-safe orchestrator",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "context_text": {"type": "string"},
                    "payload": {"type": "object"},
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="get_profile_summary",
            description="Get FHIR patient profile summary for the authenticated user",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="query_fhir_records",
            description="Query tenant-scoped FHIR resources for the authenticated user",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_type": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                },
                "required": [],
            },
        ),
        Tool(
            name="search_clinical_knowledge",
            description="Search clinical knowledge base and optional org intelligence",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
                    "include_org_intelligence": {"type": "boolean"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_audit_summary",
            description="Get recent audit events for the tenant (auditor scope required)",
            inputSchema={
                "type": "object",
                "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 200}},
                "required": [],
            },
        ),
    ]


async def _dispatch(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    ctx = resolve_auth_context()
    if name == "list_commands":
        return (await mcp_tools.list_commands(ctx)).model_dump()
    if name == "execute_command":
        body = ExecuteCommandInput(**arguments)
        return (await mcp_tools.execute_command(ctx, body)).model_dump()
    if name == "get_profile_summary":
        return (await mcp_tools.get_profile_summary(ctx)).model_dump()
    if name == "query_fhir_records":
        body = QueryFhirInput(**arguments)
        return (await mcp_tools.query_fhir_records(ctx, body)).model_dump()
    if name == "search_clinical_knowledge":
        body = SearchKnowledgeInput(**arguments)
        return (await mcp_tools.search_clinical_knowledge(ctx, body)).model_dump()
    if name == "get_audit_summary":
        limit = int(arguments.get("limit", 50))
        return (await mcp_tools.get_audit_summary(ctx, limit=limit)).model_dump()
    raise ValueError(f"Unknown tool: {name}")


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
