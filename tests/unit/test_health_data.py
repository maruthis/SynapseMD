"""Unit tests for HealthDataService and store adapters."""

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from synapsemd_platform.adapters.dual import DualHealthAdapter
from synapsemd_platform.adapters.legacy_json import LegacyJsonAdapter
from synapsemd_platform.adapters.postgres import PostgresHealthAdapter
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.database import Base
from synapsemd_platform.models import clinical, commands, governance, objects, tenant, trackers  # noqa: F401
from synapsemd_platform.services.health_data import (
    HealthDataService,
    build_health_adapter,
    get_health_data_service,
)


@pytest.fixture
async def sqlite_adapter() -> PostgresHealthAdapter:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    adapter = PostgresHealthAdapter(factory)
    yield adapter
    await engine.dispose()


@pytest.mark.asyncio
async def test_postgres_adapter_profile_allergy_gout_round_trip(sqlite_adapter: PostgresHealthAdapter) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    profile = await sqlite_adapter.upsert_profile(
        tenant_id, user_id, {"basic_info": {"gender": "M", "height": 175, "weight": 70, "birth_date": "1990-01-01"}}
    )
    assert profile["basic_info"]["gender"] == "M"
    loaded = await sqlite_adapter.get_profile(tenant_id, user_id)
    assert loaded is not None
    assert loaded["basic_info"]["height"] == 175

    allergy = await sqlite_adapter.add_allergy(
        tenant_id, user_id, {"allergen": {"name": "penicillin", "type": "drug"}, "severity": {"level": "severe"}}
    )
    listed = await sqlite_adapter.list_allergies(tenant_id, user_id)
    assert len(listed) == 1
    updated = await sqlite_adapter.update_allergy(tenant_id, user_id, allergy["id"], {"notes": "carry card"})
    assert updated is not None
    assert updated["notes"] == "carry card"
    assert await sqlite_adapter.delete_allergy(tenant_id, user_id, allergy["id"]) is True
    assert await sqlite_adapter.list_allergies(tenant_id, user_id) == []

    flare = await sqlite_adapter.add_gout_flare(
        tenant_id,
        user_id,
        {"joint": "ankle", "side": "left", "severity": "moderate", "status": "active", "onset": "2026-07-20"},
    )
    flares = await sqlite_adapter.list_gout_flares(tenant_id, user_id, status="active")
    assert len(flares) == 1
    resolved = await sqlite_adapter.update_gout_flare(tenant_id, user_id, flare["id"], {"status": "resolved"})
    assert resolved is not None
    assert resolved["status"] == "resolved"
    assert await sqlite_adapter.delete_gout_flare(tenant_id, user_id, flare["id"]) is True


@pytest.mark.asyncio
async def test_postgres_write_stores_fhir_projection(sqlite_adapter: PostgresHealthAdapter) -> None:
    from sqlalchemy import select

    from synapsemd_platform.models.clinical import PatientProfile
    from synapsemd_platform.models.trackers import AllergyRecord, GoutFlare

    tenant_id = uuid4()
    user_id = uuid4()
    await sqlite_adapter.upsert_profile(
        tenant_id, user_id, {"basic_info": {"gender": "F", "birth_date": "1988-04-12"}}
    )
    allergy = await sqlite_adapter.add_allergy(
        tenant_id, user_id, {"allergen": {"name": "peanut", "type": "food"}}
    )
    flare = await sqlite_adapter.add_gout_flare(
        tenant_id, user_id, {"joint": "toe", "uric_acid_mg_dl": 8.2, "status": "active"}
    )
    async with sqlite_adapter._session_factory() as session:
        profile = (
            await session.execute(
                select(PatientProfile).where(
                    PatientProfile.tenant_id == tenant_id, PatientProfile.user_id == user_id
                )
            )
        ).scalar_one()
        assert profile.fhir["resourceType"] == "Patient"
        assert profile.fhir["gender"] == "F"
        allergy_row = (
            await session.execute(
                select(AllergyRecord).where(AllergyRecord.record_id == allergy["id"])
            )
        ).scalar_one()
        assert allergy_row.fhir["resourceType"] == "AllergyIntolerance"
        assert allergy_row.fhir["code"]["text"] == "peanut"
        gout_row = (
            await session.execute(select(GoutFlare).where(GoutFlare.record_id == flare["id"]))
        ).scalar_one()
        assert gout_row.fhir["resourceType"] == "Observation"
        assert gout_row.fhir["valueQuantity"]["value"] == 8.2


@pytest.mark.asyncio
async def test_postgres_adapter_parses_messy_payloads(sqlite_adapter: PostgresHealthAdapter) -> None:
    from datetime import UTC, date, datetime

    tenant_id = uuid4()
    user_id = uuid4()
    await sqlite_adapter.upsert_profile(
        tenant_id,
        user_id,
        {"basic_info": {"height": "not-a-number", "birth_date": "not-a-date", "weight": ""}},
    )
    await sqlite_adapter.upsert_profile(
        tenant_id,
        user_id,
        {"basic_info": {"height": 180, "birth_date": date(1991, 2, 3)}},
    )
    await sqlite_adapter.add_allergy(
        tenant_id,
        user_id,
        {"id": "allergy_str", "allergen": "iodine", "type": "drug", "severity": "moderate", "status": "resolved"},
    )
    resolved = await sqlite_adapter.list_allergies(tenant_id, user_id, status="resolved")
    assert len(resolved) == 1
    await sqlite_adapter.add_gout_flare(
        tenant_id,
        user_id,
        {
            "recorded_at": datetime.now(UTC),
            "onset": datetime.now(UTC),
            "uric_acid_mg_dl": "7.8",
            "triggers": ["seafood"],
        },
    )
    await sqlite_adapter.add_gout_flare(
        tenant_id,
        user_id,
        {"recorded_at": "nope", "onset": "", "uric_acid_mg_dl": "x", "status": "active"},
    )
    await sqlite_adapter.add_gout_flare(
        tenant_id,
        user_id,
        {"recorded_at": "2026-07-01T08:30:00Z", "onset": "2026-07-01"},
    )
    assert len(await sqlite_adapter.list_gout_flares(tenant_id, user_id, status="active")) >= 1


@pytest.mark.asyncio
async def test_postgres_adapter_missing_rows(sqlite_adapter: PostgresHealthAdapter) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    assert await sqlite_adapter.get_profile(tenant_id, user_id) is None
    assert await sqlite_adapter.update_allergy(tenant_id, user_id, "missing", {}) is None
    assert await sqlite_adapter.delete_allergy(tenant_id, user_id, "missing") is False
    assert await sqlite_adapter.update_gout_flare(tenant_id, user_id, "missing", {}) is None
    assert await sqlite_adapter.delete_gout_flare(tenant_id, user_id, "missing") is False


@pytest.mark.asyncio
async def test_legacy_json_adapter_round_trip(tmp_path) -> None:
    adapter = LegacyJsonAdapter(tmp_path)
    tenant_id = uuid4()
    user_id = uuid4()
    await adapter.upsert_profile(tenant_id, user_id, {"basic_info": {"gender": "F"}})
    profile = await adapter.get_profile(tenant_id, user_id)
    assert profile is not None
    assert profile["basic_info"]["gender"] == "F"

    record = await adapter.add_allergy(tenant_id, user_id, {"allergen": {"name": "peanut", "type": "food"}})
    assert len(await adapter.list_allergies(tenant_id, user_id)) == 1
    await adapter.update_allergy(tenant_id, user_id, record["id"], {"notes": "avoid"})
    assert await adapter.delete_allergy(tenant_id, user_id, record["id"]) is True
    assert await adapter.update_allergy(tenant_id, user_id, "nope", {}) is None
    assert await adapter.delete_allergy(tenant_id, user_id, "nope") is False

    flare = await adapter.add_gout_flare(tenant_id, user_id, {"joint": "toe", "severity": "severe", "status": "active"})
    assert len(await adapter.list_gout_flares(tenant_id, user_id, status="active")) == 1
    await adapter.update_gout_flare(tenant_id, user_id, flare["id"], {"status": "resolved"})
    assert await adapter.delete_gout_flare(tenant_id, user_id, flare["id"]) is True
    assert await adapter.update_gout_flare(tenant_id, user_id, "nope", {}) is None
    assert await adapter.delete_gout_flare(tenant_id, user_id, "nope") is False
    assert await adapter.get_profile(uuid4(), uuid4()) is None


@pytest.mark.asyncio
async def test_dual_adapter_reads_json_when_postgres_empty(tmp_path, sqlite_adapter: PostgresHealthAdapter) -> None:
    json_store = LegacyJsonAdapter(tmp_path)
    tenant_id = uuid4()
    user_id = uuid4()
    await json_store.upsert_profile(tenant_id, user_id, {"basic_info": {"gender": "X"}})
    await json_store.add_allergy(tenant_id, user_id, {"allergen": {"name": "pollen", "type": "environmental"}})
    await json_store.add_gout_flare(tenant_id, user_id, {"joint": "knee", "status": "active"})
    dual = DualHealthAdapter(sqlite_adapter, json_store)
    profile = await dual.get_profile(tenant_id, user_id)
    assert profile is not None
    assert profile["basic_info"]["gender"] == "X"
    assert len(await dual.list_allergies(tenant_id, user_id)) == 1
    assert len(await dual.list_gout_flares(tenant_id, user_id)) == 1

    stored = await dual.upsert_profile(tenant_id, user_id, {"basic_info": {"gender": "M"}})
    assert stored["basic_info"]["gender"] == "M"
    assert (await dual.get_profile(tenant_id, user_id))["basic_info"]["gender"] == "M"
    allergy = await dual.add_allergy(tenant_id, user_id, {"allergen": {"name": "iodine", "type": "drug"}})
    await dual.update_allergy(tenant_id, user_id, allergy["id"], {"notes": "contrast"})
    await dual.delete_allergy(tenant_id, user_id, allergy["id"])
    flare = await dual.add_gout_flare(tenant_id, user_id, {"joint": "wrist"})
    await dual.update_gout_flare(tenant_id, user_id, flare["id"], {"status": "resolved"})
    await dual.delete_gout_flare(tenant_id, user_id, flare["id"])


@pytest.mark.asyncio
async def test_health_data_service_actions(sqlite_adapter: PostgresHealthAdapter) -> None:
    service = HealthDataService(sqlite_adapter)
    tenant_id = uuid4()
    user_id = uuid4()
    upserted = await service.execute(
        "profile", {"action": "upsert", "basic_info": {"gender": "M"}}, tenant_id, user_id
    )
    assert upserted["profile"]["basic_info"]["gender"] == "M"
    viewed = await service.execute("profile", {"action": "get"}, tenant_id, user_id)
    assert viewed["profile"]["basic_info"]["gender"] == "M"
    await service.execute(
        "profile",
        {"action": "upsert", "profile": {"basic_info": {"gender": "F"}}},
        tenant_id,
        user_id,
    )

    added = await service.execute(
        "allergy", {"action": "add", "allergen": "penicillin", "severity": "severe", "type": "drug"}, tenant_id, user_id
    )
    record_id = added["allergy"]["id"]
    listed = await service.execute("allergy", {"action": "list"}, tenant_id, user_id)
    assert listed["count"] == 1
    await service.execute("allergy", {"action": "update", "id": record_id, "notes": "card"}, tenant_id, user_id)
    await service.execute("allergy", {"action": "delete", "id": record_id}, tenant_id, user_id)

    flare = await service.execute(
        "gout", {"action": "add", "joint": "ankle", "side": "left", "severity": "mild"}, tenant_id, user_id
    )
    flare_id = flare["flare"]["id"]
    await service.execute("gout", {"action": "list"}, tenant_id, user_id)
    await service.execute("gout", {"action": "update", "id": flare_id, "status": "resolved"}, tenant_id, user_id)
    await service.execute("gout", {"action": "delete", "id": flare_id}, tenant_id, user_id)


@pytest.mark.asyncio
async def test_health_data_service_errors(sqlite_adapter: PostgresHealthAdapter) -> None:
    service = HealthDataService(sqlite_adapter)
    tenant_id = uuid4()
    user_id = uuid4()
    with pytest.raises(ValueError, match="Unsupported"):
        await service.execute("sleep", {}, tenant_id, user_id)
    with pytest.raises(ValueError, match="Unknown profile"):
        await service.execute("profile", {"action": "explode"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="Unknown allergy"):
        await service.execute("allergy", {"action": "explode"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="Unknown gout"):
        await service.execute("gout", {"action": "explode"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="requires id"):
        await service.execute("allergy", {"action": "update"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="requires id"):
        await service.execute("allergy", {"action": "delete"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="not found"):
        await service.execute("allergy", {"action": "update", "id": "x"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="not found"):
        await service.execute("allergy", {"action": "delete", "id": "x"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="requires id"):
        await service.execute("gout", {"action": "update"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="requires id"):
        await service.execute("gout", {"action": "delete"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="not found"):
        await service.execute("gout", {"action": "update", "id": "x"}, tenant_id, user_id)
    with pytest.raises(ValueError, match="not found"):
        await service.execute("gout", {"action": "delete", "id": "x"}, tenant_id, user_id)


def test_build_health_adapter_modes(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("LEGACY_DATA_ROOT", str(tmp_path))
    monkeypatch.setenv("HEALTH_STORE", "json")
    get_settings.cache_clear()
    assert isinstance(build_health_adapter(), LegacyJsonAdapter)

    monkeypatch.setenv("HEALTH_STORE", "postgres")
    get_settings.cache_clear()
    assert isinstance(build_health_adapter(), PostgresHealthAdapter)

    monkeypatch.setenv("HEALTH_STORE", "dual")
    get_settings.cache_clear()
    assert isinstance(build_health_adapter(), DualHealthAdapter)

    monkeypatch.setenv("HEALTH_STORE", "s3")
    get_settings.cache_clear()
    with pytest.raises(ValueError, match="Unknown HEALTH_STORE"):
        build_health_adapter()
    get_settings.cache_clear()


def test_get_health_data_service_default() -> None:
    get_settings.cache_clear()
    service = get_health_data_service()
    assert isinstance(service, HealthDataService)


def test_adapters_package_exports() -> None:
    from synapsemd_platform.adapters import (
        DualHealthAdapter,
        HealthStoreAdapter,
        LegacyJsonAdapter,
        PostgresHealthAdapter,
    )

    assert DualHealthAdapter
    assert HealthStoreAdapter
    assert LegacyJsonAdapter
    assert PostgresHealthAdapter
