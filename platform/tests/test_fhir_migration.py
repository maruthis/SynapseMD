import json
from pathlib import Path

from synapsemd_platform.fhir.migration import migrate_json_directory, profile_to_patient


def test_profile_to_patient():
    profile = {"basic_info": {"gender": "male", "birth_date": "1990-01-01"}}
    patient = profile_to_patient(profile, "pat-1", "tenant-1")
    assert patient["resourceType"] == "Patient"
    assert patient["id"] == "pat-1"
    assert patient["gender"] == "male"


def test_migrate_json_directory(tmp_path: Path):
    profile = {"basic_info": {"gender": "female", "birth_date": "1985-05-15"}}
    (tmp_path / "profile.json").write_text(json.dumps(profile), encoding="utf-8")
    (tmp_path / "allergies.json").write_text(json.dumps({"allergies": []}), encoding="utf-8")

    resources = migrate_json_directory(tmp_path, "tenant-1", "user-1")
    assert len(resources) >= 1
    assert resources[0]["resourceType"] == "Patient"
