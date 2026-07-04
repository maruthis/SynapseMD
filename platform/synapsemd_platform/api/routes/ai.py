from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.ai.data_adapter import TenantIsolationError
from synapsemd_platform.api.schemas import (
    AiActionResponse,
    AiAnalyzeRequest,
    AiChatRequest,
    AiPredictRequest,
    AiReportRequest,
)
from synapsemd_platform.auth.middleware import get_request_ctx
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


def _build_response(action: str, result: dict) -> AiActionResponse:
    return AiActionResponse(
        action=action,
        result=result,
        disclaimer=result.get("disclaimer"),
        human_review_required=bool(result.get("human_review_required")),
    )


async def _run_ai_action(
    action: str,
    ctx: RequestContext,
    session: AsyncSession,
    handler,
) -> AiActionResponse:
    service = AIService(session=session)
    try:
        result = await handler(service)
    except TenantIsolationError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return _build_response(action, result)


@router.get("/status", response_model=AiActionResponse)
async def ai_status(
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> AiActionResponse:
    return await _run_ai_action(
        "status",
        ctx,
        session,
        lambda service: service.status(ctx.tenant_id, ctx.user_id),
    )


@router.post("/analyze", response_model=AiActionResponse)
async def ai_analyze(
    body: AiAnalyzeRequest,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> AiActionResponse:
    return await _run_ai_action(
        "analyze",
        ctx,
        session,
        lambda service: service.analyze(
            ctx.tenant_id,
            ctx.user_id,
            time_range=body.time_range,
        ),
    )


@router.post("/predict", response_model=AiActionResponse)
async def ai_predict(
    body: AiPredictRequest,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> AiActionResponse:
    return await _run_ai_action(
        "predict",
        ctx,
        session,
        lambda service: service.predict(ctx.tenant_id, ctx.user_id, body.risk_type),
    )


@router.post("/chat", response_model=AiActionResponse)
async def ai_chat(
    body: AiChatRequest,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> AiActionResponse:
    return await _run_ai_action(
        "chat",
        ctx,
        session,
        lambda service: service.chat(ctx.tenant_id, ctx.user_id, body.query),
    )


@router.post("/report", response_model=AiActionResponse)
async def ai_report(
    body: AiReportRequest,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> AiActionResponse:
    return await _run_ai_action(
        "report",
        ctx,
        session,
        lambda service: service.report(
            ctx.tenant_id,
            ctx.user_id,
            report_type=body.report_type,
            time_range=body.time_range,
        ),
    )
