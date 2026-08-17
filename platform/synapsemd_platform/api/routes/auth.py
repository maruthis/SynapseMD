from uuid import UUID, uuid4

import hashlib

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.api.schemas import (
    BreakGlassRequest,
    ConsentUpdateRequest,
    LoginRequest,
    OidcCallbackRequest,
    OidcLoginRequest,
    OidcTokenRequest,
    RefreshRequest,
    TenantCreate,
    TenantResponse,
    TokenResponse,
    UserRegister,
    UserResponse,
)
from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.auth.break_glass import activate_break_glass
from synapsemd_platform.auth.consent import llm_processing_allowed, upsert_consent
from synapsemd_platform.auth.jwt import Role, create_access_token
from synapsemd_platform.auth.middleware import get_current_claims, get_request_ctx, require_scope
from synapsemd_platform.auth.oidc import (
    OidcClient,
    generate_pkce_pair,
    pop_oidc_state,
    put_oidc_state,
)
from synapsemd_platform.auth.policy import AuthzContext, Resource, Subject, authorize
from synapsemd_platform.auth.roles import ROLE_SCOPES, map_idp_groups_to_roles, scopes_for_roles
from synapsemd_platform.auth.sessions import create_session, issue_token_pair, rotate_refresh_token
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import get_db_session
from synapsemd_platform.models.governance import LLM_PROCESSING_PURPOSE
from synapsemd_platform.models.iam import Identity
from synapsemd_platform.models.tenant import User
from synapsemd_platform.services.tenant_service import (
    authenticate_user,
    create_tenant,
    register_user,
    scopes_for_role,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _token_response(payload: dict) -> TokenResponse:
    return TokenResponse(
        access_token=str(payload["access_token"]),
        token_type=str(payload.get("token_type", "bearer")),
        expires_in=int(payload["expires_in"]) if payload.get("expires_in") is not None else None,
        refresh_token=payload.get("refresh_token"),  # type: ignore[arg-type]
    )


def _maybe_set_refresh_cookie(response: Response, refresh_token: str | None) -> None:
    settings = get_settings()
    if not settings.auth_bff_cookies or not refresh_token:
        return
    response.set_cookie(
        key="synapsemd_refresh",
        value=refresh_token,
        httponly=True,
        secure=settings.is_production_like(),
        samesite="lax",
        max_age=settings.jwt_refresh_expire_days * 86400,
        path="/api/v1/auth",
    )


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
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    if not get_settings().password_login_enabled():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password login disabled; use OIDC",
        )
    user = await authenticate_user(
        session,
        tenant_id=body.tenant_id,
        email=body.email,
        password=body.password,
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    llm_ok = await llm_processing_allowed(session, tenant_id=user.tenant_id, user_id=user.id)
    payload = await issue_token_pair(
        session,
        user_id=user.id,
        tenant_id=user.tenant_id,
        roles=[user.role],
        scopes=scopes_for_role(user.role),
        amr=["pwd"],
        llm_processing=llm_ok,
    )
    _maybe_set_refresh_cookie(response, payload.get("refresh_token"))  # type: ignore[arg-type]
    return _token_response(payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_endpoint(
    body: RefreshRequest,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    current = await rotate_refresh_token(session, body.refresh_token)
    if current is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    result = await session.execute(select(User).where(User.id == current.user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    llm_ok = await llm_processing_allowed(session, tenant_id=user.tenant_id, user_id=user.id)
    access = create_access_token(
        user_id=user.id,
        tenant_id=user.tenant_id,
        roles=[user.role],
        scopes=scopes_for_role(user.role),
        amr=["pwd"],
        llm_processing=llm_ok,
    )
    _, refresh = await create_session(session, user_id=user.id, tenant_id=user.tenant_id)
    settings = get_settings()
    payload = {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.jwt_expire_minutes * 60,
    }
    _maybe_set_refresh_cookie(response, refresh)
    return _token_response(payload)


@router.post("/oidc/login")
async def oidc_login_endpoint(body: OidcLoginRequest) -> dict:
    settings = get_settings()
    client = OidcClient(settings)
    if not client.enabled():
        raise HTTPException(status_code=404, detail="OIDC is not configured")
    verifier, challenge = generate_pkce_pair()
    state = uuid4().hex
    redirect_uri = body.redirect_uri or settings.oidc_redirect_uri
    put_oidc_state(
        state=state,
        code_verifier=verifier,
        tenant_id=str(body.tenant_id),
        redirect_uri=redirect_uri,
    )
    return {
        "authorization_url": client.authorization_url(
            state=state,
            code_challenge=challenge,
            redirect_uri=redirect_uri,
            tenant_id=str(body.tenant_id),
        ),
        "state": state,
    }


@router.post("/oidc/callback", response_model=TokenResponse)
async def oidc_callback_endpoint(
    body: OidcCallbackRequest,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    pending = pop_oidc_state(body.state)
    if pending is None:
        raise HTTPException(status_code=400, detail="Invalid OIDC state")
    client = OidcClient()
    if not client.enabled():
        raise HTTPException(status_code=404, detail="OIDC is not configured")
    try:
        token_payload = await client.exchange_code(
            code=body.code,
            code_verifier=pending["code_verifier"],
            redirect_uri=pending["redirect_uri"],
        )
        id_token = token_payload.get("id_token")
        if not id_token:
            raise ValueError("missing id_token")
        claims = client.validate_id_token(id_token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="OIDC exchange failed") from exc
    tenant_id = UUID(pending["tenant_id"])
    user = await _upsert_oidc_user(session, tenant_id=tenant_id, claims=claims)
    amr = [str(item).lower() for item in (claims.get("amr") or ["mfa"])]
    llm_ok = await llm_processing_allowed(session, tenant_id=user.tenant_id, user_id=user.id)
    payload = await issue_token_pair(
        session,
        user_id=user.id,
        tenant_id=user.tenant_id,
        roles=[user.role],
        scopes=scopes_for_role(user.role),
        amr=amr,
        llm_processing=llm_ok,
    )
    _maybe_set_refresh_cookie(response, payload.get("refresh_token"))  # type: ignore[arg-type]
    return _token_response(payload)


@router.post("/oidc/token", response_model=TokenResponse)
async def oidc_token_exchange(
    body: OidcTokenRequest,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """JWT bearer for API/MCP: exchange a validated IdP ID token for a platform JWT."""
    client = OidcClient()
    if not client.enabled():
        raise HTTPException(status_code=404, detail="OIDC is not configured")
    try:
        claims = client.validate_id_token(body.id_token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid ID token") from exc
    user = await _upsert_oidc_user(session, tenant_id=body.tenant_id, claims=claims)
    amr = [str(item).lower() for item in (claims.get("amr") or [])]
    llm_ok = await llm_processing_allowed(session, tenant_id=user.tenant_id, user_id=user.id)
    payload = await issue_token_pair(
        session,
        user_id=user.id,
        tenant_id=user.tenant_id,
        roles=[user.role],
        scopes=scopes_for_role(user.role),
        amr=amr or ["pwd"],
        llm_processing=llm_ok,
    )
    _maybe_set_refresh_cookie(response, payload.get("refresh_token"))  # type: ignore[arg-type]
    return _token_response(payload)


@router.put("/consent")
async def update_consent_endpoint(
    body: ConsentUpdateRequest,
    claims=Depends(get_current_claims),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    await upsert_consent(
        session,
        tenant_id=claims.org,
        user_id=claims.sub,
        purpose=body.purpose,
        granted=body.granted,
    )
    llm_ok = body.granted if body.purpose == LLM_PROCESSING_PURPOSE else claims.llm_processing
    token = create_access_token(
        user_id=claims.sub,
        tenant_id=claims.org,
        roles=claims.roles,
        scopes=claims.scope,
        amr=claims.amr,
        purpose=claims.purpose,
        llm_processing=llm_ok,
    )
    return {"purpose": body.purpose, "granted": body.granted, "access_token": token}


@router.post("/break-glass", response_model=TokenResponse)
async def break_glass_endpoint(
    body: BreakGlassRequest,
    response: Response,
    ctx: RequestContext = Depends(get_request_ctx),
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    decision = authorize(
        Subject.from_context(ctx),
        "activate",
        Resource(type="break_glass", tenant_id=ctx.tenant_id),
        AuthzContext(purpose=ctx.purpose, llm_processing=ctx.llm_processing),
    )
    if not decision.allowed:
        await audit_producer.emit(
            AuditEventPayload(
                event_type="authz.denied",
                tenant_id=str(ctx.tenant_id),
                user_id=str(ctx.user_id),
                resource={"action": "break_glass", "reason": decision.reason},
                outcome="denied",
            )
        )
        raise HTTPException(status_code=403, detail=decision.reason)
    await activate_break_glass(
        session,
        user_id=ctx.user_id,
        tenant_id=ctx.tenant_id,
        reason=body.reason,
        minutes=body.minutes,
    )
    roles = list(ctx.roles)
    if "break_glass" not in roles:
        roles.append("break_glass")
    payload = await issue_token_pair(
        session,
        user_id=ctx.user_id,
        tenant_id=ctx.tenant_id,
        roles=roles,
        scopes=scopes_for_roles(roles),
        amr=list(ctx.amr) or ["pwd"],
        purpose=ctx.purpose,
        llm_processing=ctx.llm_processing,
    )
    _maybe_set_refresh_cookie(response, payload.get("refresh_token"))  # type: ignore[arg-type]
    result = _token_response(payload)
    return result


@router.get("/me")
async def me_endpoint(claims=Depends(get_current_claims)) -> dict:
    return {
        "user_id": str(claims.sub),
        "tenant_id": str(claims.org),
        "roles": claims.roles,
        "scopes": claims.scope,
        "amr": claims.amr,
        "purpose": claims.purpose,
        "llm_processing": claims.llm_processing,
        "available_roles": [r.value for r in Role],
        "role_scopes": {r.value: sorted(ROLE_SCOPES[r]) for r in Role},
    }


@router.get("/admin-only", dependencies=[Depends(require_scope("admin"))])
async def admin_only() -> dict:
    return {"status": "ok"}


async def _upsert_oidc_user(session: AsyncSession, *, tenant_id: UUID, claims: dict) -> User:
    issuer = str(claims.get("iss") or get_settings().oidc_issuer)
    subject = str(claims.get("sub"))
    result = await session.execute(
        select(Identity).where(Identity.issuer == issuer, Identity.subject == subject)
    )
    identity = result.scalar_one_or_none()
    if identity is not None:
        user_result = await session.execute(select(User).where(User.id == identity.user_id))
        user = user_result.scalar_one()
        return user

    groups = claims.get("groups") or claims.get("roles") or []
    if isinstance(groups, str):
        groups = [groups]
    roles = map_idp_groups_to_roles([str(g) for g in groups])
    email = str(claims.get("email") or f"{subject}@{tenant_id}.oidc")
    user = User(
        tenant_id=tenant_id,
        email_hash=hashlib.sha256(email.lower().encode()).hexdigest(),
        role=roles[0],
        password_hash=None,
    )
    session.add(user)
    await session.flush()
    session.add(
        Identity(tenant_id=tenant_id, user_id=user.id, issuer=issuer, subject=subject)
    )
    await session.commit()
    await session.refresh(user)
    return user
