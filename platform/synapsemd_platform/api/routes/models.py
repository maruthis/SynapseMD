"""Admin APIs for model catalog and tenant routing policy (D-9)."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.api.schemas import TenantModelPolicyRequest
from synapsemd_platform.auth.middleware import get_request_ctx, require_scope
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.llm.policy import DEFAULT_CATALOG
from synapsemd_platform.models.models_catalog import ModelCatalogEntry, TenantModelPolicy

router = APIRouter(prefix="/admin/models", tags=["models"])


async def ensure_catalog(session: AsyncSession) -> None:
    result = await session.execute(select(ModelCatalogEntry.model_id))
    existing = {row[0] for row in result.all()}
    if existing:
        return
    for item in DEFAULT_CATALOG:
        session.add(
            ModelCatalogEntry(
                model_id=item.model_id,
                provider=item.provider,
                display_name=item.display_name or item.model_id,
                residency=item.residency,
                baa_required=item.baa_required,
                enabled=item.enabled,
                max_tokens=item.max_tokens,
                cost_per_1k=item.cost_per_1k,
                safety_tier=item.safety_tier,
                capabilities=["chat"],
            )
        )
    await session.commit()


@router.get("", dependencies=[Depends(require_scope("admin"))])
async def list_model_catalog(session: AsyncSession = Depends(get_db_session)) -> dict:
    await ensure_catalog(session)
    result = await session.execute(select(ModelCatalogEntry).order_by(ModelCatalogEntry.model_id))
    rows = result.scalars().all()
    return {
        "models": [
            {
                "model_id": row.model_id,
                "provider": row.provider,
                "display_name": row.display_name,
                "residency": row.residency,
                "baa_required": row.baa_required,
                "enabled": row.enabled,
                "max_tokens": row.max_tokens,
                "safety_tier": row.safety_tier,
            }
            for row in rows
        ]
    }


@router.get("/policy", dependencies=[Depends(require_scope("admin"))])
async def get_tenant_model_policy(
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    row = await session.get(TenantModelPolicy, ctx.tenant_id)
    if row is None:
        return {
            "tenant_id": str(ctx.tenant_id),
            "allowlist": None,
            "residency": None,
            "baa_required": False,
            "budget_tokens_per_day": None,
            "pinned_commands": {},
        }
    return _policy_payload(row)


@router.put("/policy", dependencies=[Depends(require_scope("admin"))])
async def put_tenant_model_policy(
    body: TenantModelPolicyRequest,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    row = await session.get(TenantModelPolicy, ctx.tenant_id)
    if row is None:
        row = TenantModelPolicy(tenant_id=ctx.tenant_id)
        session.add(row)
    row.allowlist = body.allowlist
    row.residency = body.residency
    row.baa_required = body.baa_required
    row.budget_tokens_per_day = body.budget_tokens_per_day
    row.pinned_commands = body.pinned_commands
    await session.commit()
    return _policy_payload(row)


def _policy_payload(row: TenantModelPolicy) -> dict:
    return {
        "tenant_id": str(row.tenant_id),
        "allowlist": row.allowlist,
        "residency": row.residency,
        "baa_required": row.baa_required,
        "budget_tokens_per_day": row.budget_tokens_per_day,
        "pinned_commands": row.pinned_commands or {},
    }
