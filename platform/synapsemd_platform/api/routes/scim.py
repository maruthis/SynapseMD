"""SCIM 2.0 user list (E-9). Create remains unimplemented."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.auth.middleware import get_request_ctx
from synapsemd_platform.auth.policy import AuthzContext, Resource, Subject, authorize
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.models.tenant import User

router = APIRouter(prefix="/scim/v2", tags=["scim"])


def _require_scim(ctx: RequestContext) -> None:
    decision = authorize(
        Subject.from_context(ctx),
        "read",
        Resource(type="scim", tenant_id=ctx.tenant_id),
        AuthzContext(purpose=ctx.purpose, llm_processing=ctx.llm_processing),
    )
    if not decision.allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=decision.reason)


@router.get("/Users")
async def list_users(
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    _require_scim(ctx)
    result = await session.execute(select(User).where(User.tenant_id == ctx.tenant_id))
    resources = [
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": str(user.id),
            "userName": str(user.id),
            "active": user.role != "erased",
            "roles": [{"value": user.role}],
        }
        for user in result.scalars().all()
    ]
    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "startIndex": 1,
        "itemsPerPage": len(resources),
        "Resources": resources,
    }


@router.post("/Users", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_user(ctx: RequestContext = Depends(get_request_ctx)) -> dict:
    _require_scim(ctx)
    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "status": "501",
        "detail": "SCIM provisioning is not implemented",
    }
