import hashlib
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.auth.jwt import ROLE_SCOPES, Role, hash_password
from synapsemd_platform.models.tenant import Tenant, User


def _email_hash(email: str) -> str:
    return hashlib.sha256(email.lower().encode()).hexdigest()


async def create_tenant(session: AsyncSession, name: str, plan: str = "starter") -> Tenant:
    tenant = Tenant(name=name, plan=plan)
    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)
    return tenant


async def register_user(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    email: str,
    password: str,
    role: str = "patient",
) -> User:
    user = User(
        tenant_id=tenant_id,
        email_hash=_email_hash(email),
        role=role,
        password_hash=hash_password(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    email: str,
    password: str,
) -> User | None:
    from synapsemd_platform.auth.jwt import verify_password

    result = await session.execute(
        select(User).where(User.tenant_id == tenant_id, User.email_hash == _email_hash(email))
    )
    user = result.scalar_one_or_none()
    if user is None or not user.password_hash or not verify_password(password, user.password_hash):
        return None
    return user


def scopes_for_role(role: str) -> list[str]:
    try:
        return sorted(ROLE_SCOPES[Role(role)])
    except ValueError:
        return ["read:own", "write:own"]
