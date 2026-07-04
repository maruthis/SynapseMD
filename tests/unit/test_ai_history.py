from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.ai.history import record_ai_interaction
from synapsemd_platform.core.database import Base
from synapsemd_platform.models.audit import AIInteraction


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
async def test_record_ai_interaction(db_session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    interaction = await record_ai_interaction(
        db_session,
        tenant_id=tenant_id,
        user_id=user_id,
        command="ai:predict:hypertension",
        model_used="synapsemd-ai-prediction",
        result={"risk_type": "hypertension", "risk_level": "low", "probability": 0.1},
        safety_flags={"human_review_required": False},
    )
    assert interaction.tenant_id == tenant_id
    assert interaction.prompt_hash


@pytest.mark.asyncio
async def test_record_ai_interaction_all_predictions(db_session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    interaction = await record_ai_interaction(
        db_session,
        tenant_id=tenant_id,
        user_id=user_id,
        command="ai:predict:all",
        model_used="synapsemd-ai-prediction",
        result={
            "hypertension": {"risk_level": "low", "probability": 0.1},
            "diabetes": {"error": True, "message": "missing data"},
        },
    )
    assert interaction.reasoning_trace["result_summary"]["hypertension"]["risk_level"] == "low"


@pytest.mark.asyncio
async def test_record_ai_interaction_error_summary(db_session: AsyncSession) -> None:
    interaction = await record_ai_interaction(
        db_session,
        tenant_id=uuid4(),
        user_id=uuid4(),
        command="ai:predict:sleep_disorder",
        model_used="synapsemd-ai-prediction",
        result={"error": True, "message": "Insufficient sleep data"},
    )
    assert interaction.reasoning_trace["result_summary"]["error"] is True
