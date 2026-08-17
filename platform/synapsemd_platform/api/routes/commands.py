from fastapi import APIRouter, Depends, HTTPException

from synapsemd_platform.api.schemas import CommandExecuteRequest, CommandExecuteResponse
from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.auth.middleware import get_request_ctx
from synapsemd_platform.auth.policy import AuthzContext, AuthzDenied, Resource, Subject, authorize
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.llm.policy import PolicyDenied
from synapsemd_platform.models.commands import AVAILABLE_COMMANDS
from synapsemd_platform.observability.metrics import RLS_DENIAL_COUNT
from synapsemd_platform.observability.otel import get_tracer
from synapsemd_platform.services.command_orchestrator import CommandOrchestrator

router = APIRouter(prefix="/commands", tags=["commands"])
orchestrator = CommandOrchestrator()


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

    decision = authorize(
        Subject.from_context(ctx),
        "execute",
        Resource(type="command", id=body.command, tenant_id=ctx.tenant_id),
        AuthzContext(
            purpose=ctx.purpose,
            llm_processing=ctx.llm_processing,
            app_env=get_settings().app_env,
        ),
    )
    if not decision.allowed:
        if decision.reason == "cross_tenant_denied":
            RLS_DENIAL_COUNT.inc()
        await audit_producer.emit(
            AuditEventPayload(
                event_type="authz.denied",
                tenant_id=str(ctx.tenant_id),
                user_id=str(ctx.user_id),
                resource={"command": body.command, "reason": decision.reason},
                outcome="denied",
            )
        )
        raise HTTPException(status_code=403, detail=decision.reason)

    tracer = get_tracer()
    with tracer.start_as_current_span("commands.execute") as span:
        span.set_attribute("command", body.command)
        try:
            result = await orchestrator.execute(
                command=body.command,
                context_text=body.context_text,
                user_id=str(ctx.user_id),
                tenant_id=str(ctx.tenant_id),
                payload=body.payload,
                llm_processing=ctx.llm_processing,
            )
        except AuthzDenied as exc:
            await audit_producer.emit(
                AuditEventPayload(
                    event_type="authz.denied",
                    tenant_id=str(ctx.tenant_id),
                    user_id=str(ctx.user_id),
                    resource={"command": body.command, "reason": exc.reason},
                    outcome="denied",
                )
            )
            raise HTTPException(status_code=403, detail=exc.reason) from exc
        except PolicyDenied as exc:
            raise HTTPException(status_code=403, detail=exc.reason) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return CommandExecuteResponse(**{k: result[k] for k in CommandExecuteResponse.model_fields})
