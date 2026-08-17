"""DSR jobs, certificates, and legal hold (E-1–E-3)."""

from __future__ import annotations

import json
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.anonymization.engine import TokenVault
from synapsemd_platform.core.database import Base
from synapsemd_platform.jobs.audit_archive import MemoryObjectStore, archive_month
from synapsemd_platform.jobs.dsr import (
    LegalHoldActive,
    completion_certificate,
    erase_subject,
    get_object_store,
    legal_hold_active,
    object_prefix,
    process_dsr,
    set_legal_hold,
)
from synapsemd_platform.models.clinical import PatientProfile
from synapsemd_platform.models.tenant import Tenant, User
from synapsemd_platform.models.trackers import AllergyRecord


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as db:
        yield db
    await engine.dispose()


def test_certificate_schema_has_no_phi() -> None:
    cert = completion_certificate(
        request_id=uuid4(),
        tenant_id=uuid4(),
        subject_user_id=uuid4(),
        request_type="erase",
        rows_removed={"allergies": 2},
        objects_removed=1,
        tokens_removed=3,
        fhir_deleted=True,
    )
    blob = json.dumps(cert)
    assert cert["schema"] == "synapsemd.dsr.certificate.v1"
    assert "request_id" in cert
    assert "@" not in blob
    assert "MRN" not in blob
    assert "Jane" not in blob
    assert "555-0100" not in blob


@pytest.mark.asyncio
async def test_erase_removes_rows_objects_and_tokens(session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    officer = uuid4()
    session.add(Tenant(id=tenant_id, name="Clinic", plan="starter"))
    session.add(User(id=user_id, tenant_id=tenant_id, email_hash="patient", role="patient"))
    session.add(PatientProfile(tenant_id=tenant_id, user_id=user_id, payload={"basic_info": {"gender": "x"}}))
    session.add(
        AllergyRecord(
            tenant_id=tenant_id,
            user_id=user_id,
            record_id="a1",
            allergen_name="peanut",
            payload={"id": "a1"},
        )
    )
    await session.commit()

    store = get_object_store()
    prefix = object_prefix(tenant_id, user_id)
    store.put(f"{prefix}report.pdf", b"pdf")
    vault = TokenVault()
    vault.store_tokens(str(user_id), {"TOKEN_EMAIL_abc": "hidden@example.com"}, tenant_id=str(tenant_id))

    from unittest.mock import patch

    with patch("synapsemd_platform.jobs.dsr.AnonymizationEngine") as mock_engine:
        mock_engine.return_value.vault = vault
        row = await process_dsr(
            session,
            tenant_id=tenant_id,
            subject_user_id=user_id,
            requested_by=officer,
            request_type="erase",
            store=store,
        )

    assert row.status == "completed"
    assert row.certificate["fhir_deleted"] in {True, False}
    assert row.certificate["rows_removed"]["patient_profiles"] == 1
    assert row.certificate["rows_removed"]["allergies"] == 1
    assert store.objects == {}
    assert vault.delete_tokens(str(user_id), tenant_id=str(tenant_id)) == 0

    from sqlalchemy import select

    profiles = (await session.execute(select(PatientProfile))).scalars().all()
    assert profiles == []
    user = await session.get(User, user_id)
    assert user is not None
    assert user.role == "erased"


@pytest.mark.asyncio
async def test_legal_hold_blocks_erase_and_archive(session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    officer = uuid4()
    session.add(Tenant(id=tenant_id, name="Clinic", plan="starter"))
    session.add(User(id=user_id, tenant_id=tenant_id, email_hash="patient", role="patient"))
    session.add(PatientProfile(tenant_id=tenant_id, user_id=user_id, payload={"x": 1}))
    await session.commit()

    await set_legal_hold(
        session,
        tenant_id=tenant_id,
        created_by=officer,
        reason="litigation",
        user_id=user_id,
        active=True,
    )
    assert await legal_hold_active(session, tenant_id, user_id) is True

    with pytest.raises(LegalHoldActive):
        await process_dsr(
            session,
            tenant_id=tenant_id,
            subject_user_id=user_id,
            requested_by=officer,
            request_type="erase",
        )

    from sqlalchemy import select

    assert (await session.execute(select(PatientProfile))).scalars().first() is not None
    archived = archive_month(
        [{"partition_month": "2026-08"}],
        year=2026,
        month=8,
        store=MemoryObjectStore(),
        legal_hold=True,
    )
    assert archived["skipped"] is True


@pytest.mark.asyncio
async def test_access_and_correct(session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    session.add(Tenant(id=tenant_id, name="Clinic", plan="starter"))
    session.add(User(id=user_id, tenant_id=tenant_id, email_hash="patient", role="patient"))
    session.add(PatientProfile(tenant_id=tenant_id, user_id=user_id, payload={"note": "old"}))
    await session.commit()

    access = await process_dsr(
        session,
        tenant_id=tenant_id,
        subject_user_id=user_id,
        requested_by=user_id,
        request_type="access",
    )
    assert access.status == "completed"
    assert access.export_payload["profile_present"] is True
    assert "_export" not in (access.certificate or {})

    corrected = await process_dsr(
        session,
        tenant_id=tenant_id,
        subject_user_id=user_id,
        requested_by=user_id,
        request_type="correct",
        correction_payload={"profile": {"note": "new"}},
    )
    assert corrected.certificate["rows_removed"]["patient_profiles"] == 1
    from sqlalchemy import select

    profile = (await session.execute(select(PatientProfile))).scalars().one()
    assert profile.payload["note"] == "new"


@pytest.mark.asyncio
async def test_erase_subject_counts(session: AsyncSession) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    session.add(Tenant(id=tenant_id, name="Clinic", plan="starter"))
    session.add(User(id=user_id, tenant_id=tenant_id, email_hash="patient", role="patient"))
    await session.commit()
    counts = await erase_subject(session, tenant_id=tenant_id, subject_user_id=user_id)
    assert counts["rows_removed"]["users"] == 1
    await session.commit()


@pytest.mark.asyncio
async def test_unknown_dsr_type(session: AsyncSession) -> None:
    with pytest.raises(ValueError, match="Unknown DSR type"):
        await process_dsr(
            session,
            tenant_id=uuid4(),
            subject_user_id=uuid4(),
            requested_by=uuid4(),
            request_type="export",
        )


@pytest.mark.asyncio
async def test_env_legal_hold(monkeypatch: pytest.MonkeyPatch, session: AsyncSession) -> None:
    monkeypatch.setenv("AUDIT_LEGAL_HOLD", "true")
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()
    assert await legal_hold_active(session, uuid4(), uuid4()) is True
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_erase_missing_user_and_empty_correct(session: AsyncSession) -> None:
    tenant_id = uuid4()
    session.add(Tenant(id=tenant_id, name="Clinic", plan="starter"))
    await session.commit()
    counts = await erase_subject(session, tenant_id=tenant_id, subject_user_id=uuid4())
    assert counts["rows_removed"]["users"] == 0
    corrected = await process_dsr(
        session,
        tenant_id=tenant_id,
        subject_user_id=uuid4(),
        requested_by=uuid4(),
        request_type="correct",
        correction_payload={},
    )
    assert corrected.certificate["rows_removed"]["patient_profiles"] == 0
    released = await set_legal_hold(
        session,
        tenant_id=tenant_id,
        created_by=uuid4(),
        reason="none",
        active=False,
    )
    assert released.active is False
