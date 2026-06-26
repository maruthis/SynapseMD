"""OpenAPI bridge for UIs that cannot attach MCP directly (e.g. Open WebUI)."""

from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from synapsemd_platform.auth.jwt import decode_access_token
from synapsemd_platform.mcp.context import McpAuthContext
from synapsemd_platform.mcp.schemas import ExecuteCommandInput, QueryFhirInput, SearchKnowledgeInput
from synapsemd_platform.mcp import tools as mcp_tools

app = FastAPI(title="SynapseMD OpenAPI Bridge", version="0.1.0")


def _ctx_from_token(authorization: str | None) -> McpAuthContext:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    token = authorization.split(" ", 1)[1]
    claims = decode_access_token(token)
    return McpAuthContext(
        user_id=claims.sub,
        tenant_id=claims.org,
        roles=list(claims.roles),
        scopes=list(claims.scope),
    )


class ToolExecuteRequest(BaseModel):
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "synapsemd-openapi-bridge"}


@app.get("/tools")
async def list_tools() -> dict[str, list[str]]:
    return {
        "tools": [
            "list_commands",
            "execute_command",
            "get_profile_summary",
            "query_fhir_records",
            "search_clinical_knowledge",
            "get_audit_summary",
        ]
    }


@app.post("/tools/invoke")
async def invoke_tool(
    body: ToolExecuteRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    ctx = _ctx_from_token(authorization)
    name = body.tool
    args = body.arguments

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
    raise HTTPException(status_code=404, detail=f"Unknown tool: {name}")
