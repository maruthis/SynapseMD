from fastapi import APIRouter, Depends, HTTPException

from synapsemd_platform.api.schemas import CommandExecuteRequest, CommandExecuteResponse
from synapsemd_platform.auth.middleware import get_request_ctx
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.services.command_orchestrator import CommandOrchestrator

router = APIRouter(prefix="/commands", tags=["commands"])
orchestrator = CommandOrchestrator()

AVAILABLE_COMMANDS = [
    "goal", "consult", "specialist", "nutrition", "fitness", "sleep",
    "mental-health", "interaction", "profile", "query", "health-trend-analyzer",
]


@router.get("/")
async def list_commands(_: RequestContext = Depends(get_request_ctx)) -> dict:
    return {"commands": AVAILABLE_COMMANDS, "count": len(AVAILABLE_COMMANDS)}


@router.post("/execute", response_model=CommandExecuteResponse)
async def execute_command(
    body: CommandExecuteRequest,
    ctx: RequestContext = Depends(get_request_ctx),
) -> CommandExecuteResponse:
    if body.command not in AVAILABLE_COMMANDS:
        raise HTTPException(status_code=404, detail=f"Unknown command: {body.command}")

    try:
        result = await orchestrator.execute(
            command=body.command,
            context_text=body.context_text,
            user_id=str(ctx.user_id),
            tenant_id=str(ctx.tenant_id),
            payload=body.payload,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return CommandExecuteResponse(**{k: result[k] for k in CommandExecuteResponse.model_fields})
