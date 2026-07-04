from uuid import UUID

from synapsemd_platform.ai.data_adapter import TenantIsolationError
from synapsemd_platform.api.routes.commands import AVAILABLE_COMMANDS
from synapsemd_platform.audit.events import audit_producer
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore
from synapsemd_platform.mcp.context import McpAuthContext, McpAuthError, require_scope
from synapsemd_platform.mcp.schemas import (
    AiActionResult,
    AiAnalyzeInput,
    AiChatInput,
    AiPredictInput,
    AiReportInput,
    AuditSummaryResult,
    ExecuteCommandInput,
    ExecuteCommandResult,
    ListCommandsResult,
    ProfileSummaryResult,
    QueryFhirInput,
    QueryFhirResult,
    SearchKnowledgeInput,
    SearchKnowledgeResult,
    KnowledgeHit,
)
from synapsemd_platform.rag.retrieval import get_rag_engine
from synapsemd_platform.services.ai_service import AIService
from synapsemd_platform.services.command_orchestrator import CommandOrchestrator

_orchestrator = CommandOrchestrator()
_ai_service = AIService()


def _ai_action_result(action: str, result: dict) -> AiActionResult:
    return AiActionResult(
        action=action,
        result=result,
        disclaimer=result.get("disclaimer"),
        human_review_required=bool(result.get("human_review_required")),
    )


async def _run_ai_action(ctx: McpAuthContext, action: str, run) -> AiActionResult:
    require_scope(ctx, "write:own")
    try:
        result = await run()
    except TenantIsolationError as exc:
        raise McpAuthError(str(exc)) from exc
    return _ai_action_result(action, result)


async def list_commands(ctx: McpAuthContext) -> ListCommandsResult:
    require_scope(ctx, "read:own")
    return ListCommandsResult(commands=list(AVAILABLE_COMMANDS), count=len(AVAILABLE_COMMANDS))


async def execute_command(ctx: McpAuthContext, body: ExecuteCommandInput) -> ExecuteCommandResult:
    require_scope(ctx, "write:own")
    if body.command not in AVAILABLE_COMMANDS:
        raise ValueError(f"Unknown command: {body.command}")

    result = await _orchestrator.execute(
        command=body.command,
        context_text=body.context_text,
        user_id=str(ctx.user_id),
        tenant_id=str(ctx.tenant_id),
        payload=body.payload,
    )
    return ExecuteCommandResult(**{k: result[k] for k in ExecuteCommandResult.model_fields})


async def get_profile_summary(ctx: McpAuthContext) -> ProfileSummaryResult:
    require_scope(ctx, "read:own")
    store = FHIRLocalStore(get_settings().fhir_local_store)
    dal = DataAccessLayer(store)
    resources = await dal.get_patient_resources(ctx.tenant_id, ctx.user_id)
    patient = next((r for r in resources if r.get("resourceType") == "Patient"), None)
    return ProfileSummaryResult(
        patient_id=str(ctx.user_id),
        gender=patient.get("gender") if patient else None,
        birth_date=patient.get("birthDate") if patient else None,
        resource_count=len(resources),
    )


async def query_fhir_records(ctx: McpAuthContext, body: QueryFhirInput) -> QueryFhirResult:
    require_scope(ctx, "read:own")
    store = FHIRLocalStore(get_settings().fhir_local_store)
    dal = DataAccessLayer(store)
    resources = await dal.get_patient_resources(ctx.tenant_id, ctx.user_id)
    if body.resource_type:
        resources = [r for r in resources if r.get("resourceType") == body.resource_type]
    limited = resources[: body.limit]
    return QueryFhirResult(resources=limited, count=len(limited))


async def search_clinical_knowledge(
    ctx: McpAuthContext, body: SearchKnowledgeInput
) -> SearchKnowledgeResult:
    require_scope(ctx, "read:own")
    rag = get_rag_engine()
    chunks = rag.retrieve(
        body.query,
        top_k=body.top_k,
        tenant_id=str(ctx.tenant_id),
        include_org=body.include_org_intelligence,
    )
    hits = [
        KnowledgeHit(id=c.id, source=c.source, text=c.text, score=c.metadata.get("score"))
        for c in chunks
    ]
    return SearchKnowledgeResult(hits=hits, count=len(hits))


async def get_audit_summary(ctx: McpAuthContext, limit: int = 50) -> AuditSummaryResult:
    require_scope(ctx, "audit")
    events = [
        e for e in audit_producer.get_events(tenant_id=str(ctx.tenant_id))
    ][-limit:]
    return AuditSummaryResult(events=events, count=len(events))


async def ai_status(ctx: McpAuthContext) -> AiActionResult:
    require_scope(ctx, "read:own")
    try:
        result = await _ai_service.status(ctx.tenant_id, ctx.user_id)
    except TenantIsolationError as exc:
        raise McpAuthError(str(exc)) from exc
    return _ai_action_result("status", result)


async def ai_predict(ctx: McpAuthContext, body: AiPredictInput) -> AiActionResult:
    return await _run_ai_action(
        ctx,
        "predict",
        lambda: _ai_service.predict(ctx.tenant_id, ctx.user_id, body.risk_type),
    )


async def ai_analyze(ctx: McpAuthContext, body: AiAnalyzeInput) -> AiActionResult:
    return await _run_ai_action(
        ctx,
        "analyze",
        lambda: _ai_service.analyze(ctx.tenant_id, ctx.user_id, time_range=body.time_range),
    )


async def ai_chat(ctx: McpAuthContext, body: AiChatInput) -> AiActionResult:
    return await _run_ai_action(
        ctx,
        "chat",
        lambda: _ai_service.chat(ctx.tenant_id, ctx.user_id, body.query),
    )


async def ai_report(ctx: McpAuthContext, body: AiReportInput) -> AiActionResult:
    return await _run_ai_action(
        ctx,
        "report",
        lambda: _ai_service.report(
            ctx.tenant_id,
            ctx.user_id,
            report_type=body.report_type,
            time_range=body.time_range,
        ),
    )
