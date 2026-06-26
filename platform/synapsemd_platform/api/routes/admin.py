from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.api.schemas import MigrateRequest, ReviewDecisionRequest
from synapsemd_platform.audit.events import audit_producer
from synapsemd_platform.auth.middleware import get_request_ctx, require_scope
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore, migrate_json_directory
from synapsemd_platform.models.review import ReviewQueueItem
from synapsemd_platform.observability.metrics import REQUEST_COUNT

router = APIRouter(tags=["admin"])


@router.get("/health")
async def health() -> dict:
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
    return {"status": "healthy", "service": "synapsemd-platform"}


@router.get("/metrics")
async def metrics() -> dict:
    from prometheus_client import generate_latest

    return {"metrics": generate_latest().decode("utf-8", errors="replace")}


@router.post("/admin/migrate", dependencies=[Depends(require_scope("admin"))])
async def migrate_data(
    body: MigrateRequest,
    ctx: RequestContext = Depends(get_request_ctx),
) -> dict:
    source = Path(body.source_directory)
    resources = migrate_json_directory(source, str(ctx.tenant_id), str(ctx.user_id))
    store = FHIRLocalStore(get_settings().fhir_local_store)
    dal = DataAccessLayer(store)
    await dal.upsert_resources(ctx.tenant_id, ctx.user_id, resources)
    return {"migrated_resources": len(resources), "resource_types": [r["resourceType"] for r in resources]}


@router.get("/admin/audit", dependencies=[Depends(require_scope("audit"))])
async def list_audit_events(ctx: RequestContext = Depends(get_request_ctx)) -> dict:
    events = audit_producer.get_events(tenant_id=str(ctx.tenant_id))
    return {"events": events}


@router.get("/review/queue", dependencies=[Depends(require_scope("read:org"))])
async def review_queue(session: AsyncSession = Depends(get_db_session)) -> dict:
    result = await session.execute(
        select(ReviewQueueItem).where(ReviewQueueItem.status == "pending")
    )
    items = result.scalars().all()
    return {
        "pending": [
            {
                "id": str(i.id),
                "command": i.command,
                "interaction_id": str(i.interaction_id),
                "ai_response": i.ai_response,
            }
            for i in items
        ]
    }


@router.post("/review/{item_id}/decide", dependencies=[Depends(require_scope("read:org"))])
async def decide_review(
    item_id: UUID,
    body: ReviewDecisionRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    result = await session.execute(select(ReviewQueueItem).where(ReviewQueueItem.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        return {"error": "not found"}
    item.status = body.action
    item.clinician_notes = body.clinician_notes
    if body.modified_response:
        item.ai_response = body.modified_response
    await session.commit()
    return {"id": str(item.id), "status": item.status}
