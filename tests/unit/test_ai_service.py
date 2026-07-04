import json
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.ai.data_adapter import HealthDataContext
from synapsemd_platform.core.database import Base
from synapsemd_platform.services.ai_service import AIService


@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.fixture
def low_risk_profile() -> dict:
    birth = (datetime.now() - timedelta(days=365 * 30)).strftime("%Y-%m-%d")
    return {
        "basic_info": {"birth_date": birth, "gender": "female"},
        "calculated": {"bmi": 22},
        "lifestyle": {"activity_level": "moderate", "smoking": False},
        "family_history": {},
        "medical_history": {},
        "vitals": {"blood_pressure": [{"systolic": 115, "diastolic": 75}]},
        "lab_results": {"fasting_glucose": [{"value": 5.0}]},
    }


@pytest.fixture
def mock_adapter(low_risk_profile: dict):
    tenant_id = uuid4()
    user_id = uuid4()

    class MockAdapter:
        async def load(self, load_tenant_id, load_user_id):
            return HealthDataContext(
                tenant_id=load_tenant_id,
                user_id=load_user_id,
                user_profile=low_risk_profile,
                nutrition_data={"daily_records": [{"nutrients": {"vitamin_d": {"rda_ratio": 0.9}}}]},
                sleep_data={
                    "sleep_records": [
                        {
                            "sleep_quality": {"subjective_quality": "good"},
                            "sleep_metrics": {"sleep_duration_hours": 7.5, "sleep_efficiency": 90},
                        }
                    ]
                    * 7
                },
                fhir_resources=[],
                data_sources=["mock:profile"],
            )

    return MockAdapter(), tenant_id, user_id


@pytest.mark.asyncio
async def test_ai_service_status(mock_adapter) -> None:
    adapter, tenant_id, user_id = mock_adapter
    service = AIService(adapter=adapter)
    status = await service.status(tenant_id, user_id)
    assert status["enabled"] is True
    assert "hypertension" in status["supported_risks"]
    assert status["disclaimer"]


@pytest.mark.asyncio
async def test_ai_service_predict(mock_adapter) -> None:
    adapter, tenant_id, user_id = mock_adapter
    service = AIService(adapter=adapter)
    result = await service.predict(tenant_id, user_id, "hypertension")
    assert result["risk_type"] == "hypertension"
    assert result["disclaimer"]
    assert "human_review_required" in result


@pytest.mark.asyncio
async def test_ai_service_analyze(mock_adapter) -> None:
    adapter, tenant_id, user_id = mock_adapter
    service = AIService(adapter=adapter)
    result = await service.analyze(tenant_id, user_id)
    assert "predictions" in result
    assert "summary" in result
    assert result["disclaimer"]


@pytest.mark.asyncio
async def test_ai_service_chat(mock_adapter) -> None:
    adapter, tenant_id, user_id = mock_adapter
    service = AIService(adapter=adapter)
    result = await service.chat(tenant_id, user_id, "How is my sleep?")
    assert result["response"]
    assert result["disclaimer"]


@pytest.mark.asyncio
async def test_ai_service_report(mock_adapter) -> None:
    adapter, tenant_id, user_id = mock_adapter
    service = AIService(adapter=adapter)
    result = await service.report(tenant_id, user_id, report_type="comprehensive")
    assert result["report_type"] == "comprehensive"
    assert "analysis" in result


@pytest.mark.asyncio
async def test_ai_service_predict_with_session(mock_adapter, db_session: AsyncSession) -> None:
    adapter, tenant_id, user_id = mock_adapter
    service = AIService(adapter=adapter, session=db_session)
    result = await service.predict(tenant_id, user_id, "hypertension")
    assert result["risk_type"] == "hypertension"


@pytest.mark.asyncio
async def test_ai_service_predict_error_enrichment(mock_adapter) -> None:
    class EmptyAdapter:
        async def load(self, load_tenant_id, load_user_id):
            return HealthDataContext(
                tenant_id=load_tenant_id,
                user_id=load_user_id,
                user_profile={},
                nutrition_data=None,
                sleep_data=None,
                fhir_resources=[],
                data_sources=[],
            )

    service = AIService(adapter=EmptyAdapter())
    tenant_id = uuid4()
    user_id = uuid4()
    result = await service.predict(tenant_id, user_id, "hypertension")
    assert result["error"] is True
    assert result["disclaimer"]


@pytest.mark.asyncio
async def test_ai_service_chat_guardrail_block(mock_adapter, monkeypatch) -> None:
    from synapsemd_platform.governance.guardrails import GuardrailResult

    adapter, tenant_id, user_id = mock_adapter
    service = AIService(adapter=adapter)
    blocked = GuardrailResult(
        blocked=True,
        safe_fallback="Blocked for safety.",
        requires_disclaimer=False,
        human_review_queued=True,
        disclaimer=None,
    )
    monkeypatch.setattr(service.guardrails, "validate", lambda *args, **kwargs: blocked)
    result = await service.chat(tenant_id, user_id, "Tell me my diagnosis")
    assert result["blocked"] is True
    assert result["response"] == "Blocked for safety."
