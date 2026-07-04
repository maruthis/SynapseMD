from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.api.schemas import MigrateRequest, ReviewDecisionRequest
from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.auth.middleware import get_request_ctx, require_scope
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore, migrate_json_directory
from synapsemd_platform.models.review import ReviewQueueItem
from synapsemd_platform.models.tenant import User
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


async def _get_tenant_user(
    session: AsyncSession,
    tenant_id: UUID,
    user_id: UUID,
) -> User:
    result = await session.execute(
        select(User).where(User.id == user_id, User.tenant_id == tenant_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found in tenant")
    return user


@router.get("/admin/export/{user_id}", dependencies=[Depends(require_scope("admin"))])
async def export_user_data(
    user_id: UUID,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    await _get_tenant_user(session, ctx.tenant_id, user_id)
    store = FHIRLocalStore(get_settings().fhir_local_store)
    dal = DataAccessLayer(store)
    resources = await dal.get_patient_resources(ctx.tenant_id, user_id)
    await audit_producer.emit(
        AuditEventPayload(
            event_type="admin.export",
            tenant_id=str(ctx.tenant_id),
            user_id=str(ctx.user_id),
            resource={"exported_user_id": str(user_id), "resource_count": len(resources)},
            outcome="success",
        )
    )
    return {
        "tenant_id": str(ctx.tenant_id),
        "user_id": str(user_id),
        "format": "fhir-bundle",
        "resource_count": len(resources),
        "resources": resources,
    }


@router.post("/admin/users/{user_id}/erase", dependencies=[Depends(require_scope("admin"))])
async def erase_user_data(
    user_id: UUID,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    user = await _get_tenant_user(session, ctx.tenant_id, user_id)
    if user.role == "erased":
        return {"user_id": str(user_id), "status": "already_erased"}

    store = FHIRLocalStore(get_settings().fhir_local_store)
    dal = DataAccessLayer(store)
    deleted = await dal.delete_patient_resources(ctx.tenant_id, user_id)
    user.role = "erased"
    user.password_hash = None
    await session.commit()

    await audit_producer.emit(
        AuditEventPayload(
            event_type="admin.erase",
            tenant_id=str(ctx.tenant_id),
            user_id=str(ctx.user_id),
            resource={"erased_user_id": str(user_id), "fhir_deleted": deleted},
            outcome="success",
        )
    )
    return {"user_id": str(user_id), "status": "erased", "fhir_deleted": deleted}


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
