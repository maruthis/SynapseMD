from uuid import uuid4

import pytest

from synapsemd_platform.ai.data_adapter import TenantHealthDataAdapter, TenantIsolationError
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore, profile_to_patient


@pytest.mark.asyncio
async def test_ai_adapter_cross_tenant_blocked(tmp_path) -> None:
    tenant_a = uuid4()
    tenant_b = uuid4()
    user_id = uuid4()

    store = FHIRLocalStore(str(tmp_path / "fhir"))
    dal = DataAccessLayer(store)

    patient = profile_to_patient(
        {"basic_info": {"gender": "male", "birth_date": "1985-01-01"}},
        str(user_id),
        str(tenant_b),
    )
    await dal.upsert_resources(tenant_a, user_id, [patient])

    adapter = TenantHealthDataAdapter(dal)
    with pytest.raises(TenantIsolationError):
        await adapter.load(tenant_a, user_id)

    patient_ok = profile_to_patient(
        {"basic_info": {"gender": "male", "birth_date": "1985-01-01"}},
        str(user_id),
        str(tenant_b),
    )
    await dal.upsert_resources(tenant_b, user_id, [patient_ok])
    ctx = await adapter.load(tenant_b, user_id)
    assert ctx.user_profile["basic_info"]["gender"] == "male"
