from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.auth.consent import llm_processing_allowed, upsert_consent
from synapsemd_platform.core.database import Base
from synapsemd_platform.models import governance  # noqa: F401
from synapsemd_platform.models.governance import LLM_PROCESSING_PURPOSE


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
async def test_llm_consent_default_true_in_development(db_session: AsyncSession) -> None:
    allowed = await llm_processing_allowed(db_session, tenant_id=uuid4(), user_id=uuid4())
    assert allowed is True


@pytest.mark.asyncio
async def test_llm_consent_explicit_false(db_session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    await upsert_consent(
        db_session,
        tenant_id=tenant_id,
        user_id=user_id,
        purpose=LLM_PROCESSING_PURPOSE,
        granted=False,
    )
    allowed = await llm_processing_allowed(db_session, tenant_id=tenant_id, user_id=user_id)
    assert allowed is False


@pytest.mark.asyncio
async def test_llm_consent_upsert_updates_existing(db_session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    first = await upsert_consent(
        db_session,
        tenant_id=tenant_id,
        user_id=user_id,
        purpose=LLM_PROCESSING_PURPOSE,
        granted=True,
    )
    second = await upsert_consent(
        db_session,
        tenant_id=tenant_id,
        user_id=user_id,
        purpose=LLM_PROCESSING_PURPOSE,
        granted=False,
    )
    assert first.id == second.id
    assert second.granted is False


@pytest.mark.asyncio
async def test_orchestrator_refuses_llm_without_consent() -> None:
    from synapsemd_platform.auth.policy import AuthzDenied
    from synapsemd_platform.services.command_orchestrator import CommandOrchestrator

    orchestrator = CommandOrchestrator()
    with pytest.raises(AuthzDenied, match="llm_processing"):
        await orchestrator.execute(
            command="goal",
            context_text="Lose 5kg",
            user_id=str(uuid4()),
            tenant_id=str(uuid4()),
            llm_processing=False,
        )
