from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.api.schemas import (
    LoginRequest,
    TenantCreate,
    TenantResponse,
    TokenResponse,
    UserRegister,
    UserResponse,
)
from synapsemd_platform.auth.jwt import ROLE_SCOPES, Role, create_access_token
from synapsemd_platform.auth.middleware import get_current_claims, require_scope
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.services.tenant_service import (
    authenticate_user,
    create_tenant,
    register_user,
    scopes_for_role,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant_endpoint(
    body: TenantCreate,
    session: AsyncSession = Depends(get_db_session),
) -> TenantResponse:
    tenant = await create_tenant(session, body.name, body.plan)
    return TenantResponse(id=tenant.id, name=tenant.name, plan=tenant.plan)


@router.post("/tenants/{tenant_id}/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(
    tenant_id: UUID,
    body: UserRegister,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    if body.role not in {r.value for r in Role}:
        raise HTTPException(status_code=400, detail="Invalid role")
    user = await register_user(
        session,
        tenant_id=tenant_id,
        email=body.email,
        password=body.password,
        role=body.role,
    )
    return UserResponse(id=user.id, tenant_id=user.tenant_id, role=user.role)


@router.post("/login", response_model=TokenResponse)
async def login_endpoint(
    body: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    user = await authenticate_user(
        session,
        tenant_id=body.tenant_id,
        email=body.email,
        password=body.password,
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        user_id=user.id,
        tenant_id=user.tenant_id,
        roles=[user.role],
        scopes=scopes_for_role(user.role),
    )
    return TokenResponse(access_token=token)


@router.get("/me")
async def me_endpoint(claims=Depends(get_current_claims)) -> dict:
    return {
        "user_id": str(claims.sub),
        "tenant_id": str(claims.org),
        "roles": claims.roles,
        "scopes": claims.scope,
        "available_roles": [r.value for r in Role],
        "role_scopes": {r.value: sorted(ROLE_SCOPES[r]) for r in Role},
    }


@router.get("/admin-only", dependencies=[Depends(require_scope("admin"))])
async def admin_only() -> dict:
    return {"status": "ok"}
