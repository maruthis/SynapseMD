import json
from pathlib import Path
from uuid import uuid4

import pytest

from synapsemd_platform.fhir.migration import (
    DataAccessLayer,
    FHIRLocalStore,
    FHIR_MAPPINGS,
    allergies_to_fhir,
    migrate_json_directory,
    observation_from_tracker,
    profile_to_patient,
)


def test_fhir_mappings_defined() -> None:
    assert "profile.json" in FHIR_MAPPINGS


def test_profile_to_patient() -> None:
    profile = {"basic_info": {"gender": "female", "birth_date": "1985-01-01"}}
    patient = profile_to_patient(profile, "p1", "t1")
    assert patient["resourceType"] == "Patient"
    assert patient["gender"] == "female"


def test_allergies_to_fhir() -> None:
    doc = {"allergies": [{"allergen": "Penicillin", "severity": "high"}]}
    resources = allergies_to_fhir(doc, "Patient/p1")
    assert resources[0]["resourceType"] == "AllergyIntolerance"
    assert resources[0]["code"]["text"] == "Penicillin"


def test_allergies_to_fhir_name_fallback() -> None:
    doc = {"allergies": [{"name": "Peanuts"}]}
    resources = allergies_to_fhir(doc, "Patient/p1")
    assert resources[0]["code"]["text"] == "Peanuts"


def test_observation_from_tracker() -> None:
    obs = observation_from_tracker(
        {"value": {"value": 120, "unit": "mmHg"}},
        patient_ref="Patient/p1",
        loinc_code="85354-9",
        display="Blood pressure",
    )
    assert obs["resourceType"] == "Observation"


@pytest.mark.asyncio
async def test_fhir_local_store_roundtrip(tmp_path: Path) -> None:
    store = FHIRLocalStore(str(tmp_path))
    tenant_id = uuid4()
    user_id = uuid4()
    resources = [{"resourceType": "Patient", "id": "p1"}]

    await store.save_bundle(tenant_id, user_id, resources)
    loaded = await store.load_bundle(tenant_id, user_id)
    assert loaded[0]["id"] == "p1"


@pytest.mark.asyncio
async def test_fhir_local_store_empty(tmp_path: Path) -> None:
    store = FHIRLocalStore(str(tmp_path))
    assert await store.load_bundle(uuid4(), uuid4()) == []


@pytest.mark.asyncio
async def test_data_access_layer_upsert(tmp_path: Path) -> None:
    store = FHIRLocalStore(str(tmp_path))
    dal = DataAccessLayer(store)
    tenant_id = uuid4()
    user_id = uuid4()
    await dal.upsert_resources(tenant_id, user_id, [{"resourceType": "Patient", "id": "p1"}])
    await dal.upsert_resources(tenant_id, user_id, [{"resourceType": "Observation", "id": "o1"}])
    resources = await dal.get_patient_resources(tenant_id, user_id)
    assert len(resources) == 2


def test_migrate_json_directory(tmp_path: Path) -> None:
    (tmp_path / "profile.json").write_text(
        json.dumps({"basic_info": {"gender": "male"}}), encoding="utf-8"
    )
    (tmp_path / "allergies.json").write_text(json.dumps({"allergies": []}), encoding="utf-8")
    resources = migrate_json_directory(tmp_path, "tenant-1", "user-1")
    assert any(r["resourceType"] == "Patient" for r in resources)
