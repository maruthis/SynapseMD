import argparse
import importlib.util
import json
import sys
from pathlib import Path
from uuid import UUID

import pytest


def _load_migrate_module():
    path = Path(__file__).resolve().parents[2] / "platform" / "scripts" / "migrate_json_to_fhir.py"
    spec = importlib.util.spec_from_file_location("migrate_json_to_fhir", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.asyncio
async def test_migrate_script_main(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load_migrate_module()
    (tmp_path / "profile.json").write_text(
        json.dumps({"basic_info": {"gender": "male"}}), encoding="utf-8"
    )
    fhir_dir = tmp_path / "fhir"
    monkeypatch.setenv("FHIR_LOCAL_STORE", str(fhir_dir))

    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()

    args = argparse.Namespace(
        source=tmp_path,
        tenant_id="00000000-0000-0000-0000-000000000001",
        user_id="00000000-0000-0000-0000-000000000002",
    )
    monkeypatch.setattr(module.argparse.ArgumentParser, "parse_args", lambda self: args)
    await module.main()

    bundle_path = fhir_dir / args.tenant_id / f"{args.user_id}.json"
    assert bundle_path.exists()
