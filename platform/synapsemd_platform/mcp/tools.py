from uuid import UUID

from synapsemd_platform.api.routes.commands import AVAILABLE_COMMANDS
from synapsemd_platform.audit.events import audit_producer
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore
from synapsemd_platform.mcp.context import McpAuthContext, require_scope
from synapsemd_platform.mcp.schemas import (
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
from synapsemd_platform.services.command_orchestrator import CommandOrchestrator

_orchestrator = CommandOrchestrator()


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
        e for e in audit_producer.get_events() if e.get("tenant_id") == str(ctx.tenant_id)
    ][-limit:]
    return AuditSummaryResult(events=events, count=len(events))
