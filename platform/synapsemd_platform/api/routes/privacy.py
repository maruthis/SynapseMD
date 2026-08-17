"""Privacy officer APIs: DSR workflow and legal hold (E-1–E-3)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.api.schemas import DsrCreateRequest, LegalHoldRequest
from synapsemd_platform.auth.middleware import get_request_ctx
from synapsemd_platform.auth.policy import AuthzContext, Resource, Subject, authorize
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.core.rls import set_rls_context
from synapsemd_platform.jobs.dsr import LegalHoldActive, process_dsr, set_legal_hold
from synapsemd_platform.models.governance import DsrRequest, LegalHold
from synapsemd_platform.models.tenant import User

router = APIRouter(prefix="/privacy", tags=["privacy"])


def _require_privacy(ctx: RequestContext) -> None:
    decision = authorize(
        Subject.from_context(ctx),
        "write",
        Resource(type="privacy", tenant_id=ctx.tenant_id),
        AuthzContext(purpose=ctx.purpose, llm_processing=ctx.llm_processing),
    )
    if not decision.allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=decision.reason)


async def _prepare(ctx: RequestContext, session: AsyncSession) -> None:
    _require_privacy(ctx)
    await set_rls_context(session, ctx.tenant_id, ctx.user_id)


def _certificate_payload(row: DsrRequest) -> dict:
    cert = dict(row.certificate or {})
    cert.pop("_export", None)
    return cert


def _dsr_payload(row: DsrRequest, *, include_export: bool = False) -> dict:
    body = {
        "id": str(row.id),
        "tenant_id": str(row.tenant_id),
        "subject_user_id": str(row.subject_user_id),
        "request_type": row.request_type,
        "status": row.status,
        "certificate": _certificate_payload(row),
        "completed_at": row.completed_at.isoformat() if row.completed_at else None,
    }
    export = getattr(row, "export_payload", None)
    if include_export and export is not None:
        body["export"] = export
    return body


@router.post("/dsr")
async def create_dsr(
    body: DsrCreateRequest,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    await _prepare(ctx, session)
    subject = await session.execute(
        select(User).where(User.id == body.subject_user_id, User.tenant_id == ctx.tenant_id)
    )
    if subject.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="User not found in tenant")
    try:
        row = await process_dsr(
            session,
            tenant_id=ctx.tenant_id,
            subject_user_id=body.subject_user_id,
            requested_by=ctx.user_id,
            request_type=body.request_type,
            correction_payload=body.correction,
        )
    except LegalHoldActive as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.reason) from exc
    return _dsr_payload(row, include_export=body.request_type == "access")


@router.get("/dsr")
async def list_dsr(
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    await _prepare(ctx, session)
    result = await session.execute(
        select(DsrRequest)
        .where(DsrRequest.tenant_id == ctx.tenant_id)
        .order_by(DsrRequest.created_at.desc())
    )
    return {"requests": [_dsr_payload(row) for row in result.scalars().all()]}


@router.get("/dsr/{request_id}")
async def get_dsr(
    request_id: UUID,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    await _prepare(ctx, session)
    row = await session.get(DsrRequest, request_id)
    if row is None or row.tenant_id != ctx.tenant_id:
        raise HTTPException(status_code=404, detail="DSR not found")
    return _dsr_payload(row)


@router.post("/legal-hold")
async def upsert_legal_hold(
    body: LegalHoldRequest,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    await _prepare(ctx, session)
    hold = await set_legal_hold(
        session,
        tenant_id=ctx.tenant_id,
        created_by=ctx.user_id,
        reason=body.reason,
        user_id=body.user_id,
        active=body.active,
    )
    return {
        "id": str(hold.id),
        "tenant_id": str(hold.tenant_id),
        "user_id": str(hold.user_id) if hold.user_id else None,
        "active": hold.active,
        "reason": hold.reason,
    }


@router.get("/legal-hold")
async def list_legal_holds(
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    await _prepare(ctx, session)
    result = await session.execute(
        select(LegalHold)
        .where(LegalHold.tenant_id == ctx.tenant_id)
        .order_by(LegalHold.created_at.desc())
    )
    return {
        "holds": [
            {
                "id": str(row.id),
                "user_id": str(row.user_id) if row.user_id else None,
                "active": row.active,
                "reason": row.reason,
            }
            for row in result.scalars().all()
        ]
    }
