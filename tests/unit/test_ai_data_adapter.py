import json
from uuid import uuid4

import pytest

from synapsemd_platform.ai.config_store import TenantAIConfigStore
from synapsemd_platform.ai.data_adapter import TenantHealthDataAdapter, TenantIsolationError
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore, profile_to_patient


@pytest.fixture
def tenant_id():
    return uuid4()


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def dal(tmp_path):
    store = FHIRLocalStore(str(tmp_path / "fhir"))
    return DataAccessLayer(store)


@pytest.mark.asyncio
async def test_adapter_loads_fhir_observations(dal, tenant_id, user_id) -> None:
    profile = {"basic_info": {"gender": "male", "birth_date": "1980-01-01"}}
    patient = profile_to_patient(profile, str(user_id), str(tenant_id))
    observation = {
        "resourceType": "Observation",
        "code": {"coding": [{"code": "8480-6"}]},
        "valueQuantity": {"value": 135},
    }
    glucose_obs = {
        "resourceType": "Observation",
        "code": {"coding": [{"code": "2339-0"}]},
        "valueQuantity": {"value": 5.8},
    }
    await dal.upsert_resources(tenant_id, user_id, [patient, observation, glucose_obs])

    adapter = TenantHealthDataAdapter(dal, legacy_data_root="/nonexistent")
    ctx = await adapter.load(tenant_id, user_id)
    assert ctx.user_profile["vitals"]["blood_pressure"][0]["systolic"] == 135
    assert ctx.user_profile["lab_results"]["fasting_glucose"][0]["value"] == 5.8


@pytest.mark.asyncio
async def test_adapter_loads_legacy_json(dal, tenant_id, user_id, tmp_path) -> None:
    legacy_dir = tmp_path / "data" / str(tenant_id) / str(user_id)
    legacy_dir.mkdir(parents=True)
    (legacy_dir / "profile.json").write_text(
        json.dumps({"basic_info": {"gender": "male"}, "calculated": {"bmi": 25}}),
        encoding="utf-8",
    )
    adapter = TenantHealthDataAdapter(dal, legacy_data_root=tmp_path / "data")
    ctx = await adapter.load(tenant_id, user_id)
    assert ctx.user_profile["calculated"]["bmi"] == 25
    assert "legacy:profile.json" in ctx.data_sources


@pytest.mark.asyncio
async def test_adapter_rejects_cross_tenant_fhir(dal, tenant_id, user_id) -> None:
    other_tenant = uuid4()
    profile = {"basic_info": {"gender": "male", "birth_date": "1980-01-01"}}
    patient = profile_to_patient(profile, str(user_id), str(other_tenant))
    await dal.upsert_resources(tenant_id, user_id, [patient])

    adapter = TenantHealthDataAdapter(dal)
    with pytest.raises(TenantIsolationError):
        await adapter.load(tenant_id, user_id)


def test_config_store_defaults(tenant_id) -> None:
    store = TenantAIConfigStore(config_dir="/nonexistent")
    config = store.resolve(tenant_id)
    assert config["ai_features"]["enabled"] is True


def test_config_store_file_override(tenant_id, tmp_path) -> None:
    config_dir = tmp_path / "ai-config"
    config_dir.mkdir()
    (config_dir / f"{tenant_id}.json").write_text(
        json.dumps({"ai_features": {"model_version": "v2.5"}}),
        encoding="utf-8",
    )
    store = TenantAIConfigStore(config_dir=config_dir)
    config = store.resolve(tenant_id)
    assert config["ai_features"]["model_version"] == "v2.5"


def test_config_store_db_override(tenant_id) -> None:
    store = TenantAIConfigStore(config_dir="/nonexistent")
    config = store.resolve(tenant_id, {"ai_features": {"predictions": {"enabled": False}}})
    assert config["ai_features"]["predictions"]["enabled"] is False
