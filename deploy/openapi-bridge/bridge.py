"""OpenAPI bridge for UIs that cannot attach MCP directly (e.g. Open WebUI)."""

from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from synapsemd_platform.auth.jwt import decode_access_token
from synapsemd_platform.mcp.context import McpAuthContext, McpAuthError
from synapsemd_platform.mcp.dispatch import MCP_TOOL_NAMES, dispatch_tool

app = FastAPI(title="SynapseMD OpenAPI Bridge", version="0.1.0")


def _ctx_from_token(authorization: str | None) -> McpAuthContext:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        claims = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
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
    return {"tools": MCP_TOOL_NAMES}


@app.post("/tools/invoke")
async def invoke_tool(
    body: ToolExecuteRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    ctx = _ctx_from_token(authorization)
    try:
        return await dispatch_tool(body.tool, ctx, body.arguments)
    except McpAuthError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
