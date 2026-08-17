from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.auth.break_glass import activate_break_glass, is_grant_active
from synapsemd_platform.auth.sessions import create_session, hash_refresh_token, rotate_refresh_token
from synapsemd_platform.core.database import Base
from synapsemd_platform.models import iam  # noqa: F401


@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_refresh_rotation(db_session: AsyncSession) -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    session_row, raw = await create_session(db_session, user_id=user_id, tenant_id=tenant_id)
    assert session_row.refresh_token_hash == hash_refresh_token(raw)
    rotated = await rotate_refresh_token(db_session, raw)
    assert rotated is not None
    assert rotated.revoked_at is not None
    again = await rotate_refresh_token(db_session, raw)
    assert again is None


@pytest.mark.asyncio
async def test_break_glass_grant_and_audit(db_session: AsyncSession) -> None:
    from synapsemd_platform.audit.events import audit_producer

    audit_producer._memory_events.clear()
    grant = await activate_break_glass(
        db_session,
        user_id=uuid4(),
        tenant_id=uuid4(),
        reason="emergency chart review",
        minutes=15,
    )
    assert grant.notified is True
    assert is_grant_active(grant)
    expired = grant
    expired.expires_at = datetime.now(UTC) - timedelta(minutes=1)
    assert is_grant_active(expired) is False
    events = audit_producer.get_events()
    assert any(e["event_type"] == "auth.break_glass.activated" for e in events)
