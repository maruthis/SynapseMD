"""SQLAlchemy health adapter (Postgres SoR; SQLite-compatible for unit tests)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from synapsemd_platform.core.database import async_session_factory
from synapsemd_platform.core.rls import set_rls_context
from synapsemd_platform.fhir.projection import (
    allergy_to_fhir,
    gout_flare_to_observation,
    profile_to_patient,
)
from synapsemd_platform.models.clinical import PatientProfile
from synapsemd_platform.models.trackers import AllergyRecord, GoutFlare


def _parse_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text = str(value)[:10]
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def _parse_datetime(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _profile_columns(profile: dict[str, Any]) -> dict[str, Any]:
    basic = profile.get("basic_info") or {}
    return {
        "gender": basic.get("gender"),
        "height_cm": _as_float(basic.get("height")),
        "weight_kg": _as_float(basic.get("weight")),
        "birth_date": _parse_date(basic.get("birth_date")),
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    return value


def _as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _allergy_columns(record: dict[str, Any]) -> dict[str, Any]:
    allergen = record.get("allergen") if isinstance(record.get("allergen"), dict) else {}
    severity = record.get("severity")
    severity_level = severity.get("level") if isinstance(severity, dict) else severity
    status = record.get("current_status") if isinstance(record.get("current_status"), dict) else {}
    allergen_name = (
        allergen.get("name") or record.get("allergen_name") or record.get("allergen") or "unknown"
    )
    allergen_type = (
        allergen.get("type") or record.get("allergen_type") or record.get("type") or "other"
    )
    return {
        "allergen_name": allergen_name,
        "allergen_type": allergen_type,
        "severity": str(severity_level or record.get("severity") or "unknown"),
        "status": status.get("status") or record.get("status") or "active",
    }


def _gout_columns(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "onset": _parse_date(record.get("onset")),
        "joint": record.get("joint"),
        "side": record.get("side"),
        "severity": record.get("severity") or "unknown",
        "status": record.get("status") or "active",
        "uric_acid_mg_dl": _as_float(record.get("uric_acid_mg_dl")),
        "triggers": list(record.get("triggers") or []),
        "recorded_at": _parse_datetime(record.get("recorded_at")),
    }


def _patient_ref(user_id: UUID) -> str:
    return f"Patient/{user_id}"


def _profile_fhir(profile: dict[str, Any], tenant_id: UUID, user_id: UUID) -> dict[str, Any]:
    return profile_to_patient(profile, str(user_id), str(tenant_id))


def _allergy_fhir(record: dict[str, Any], tenant_id: UUID, user_id: UUID) -> dict[str, Any]:
    return allergy_to_fhir(
        record,
        patient_ref=_patient_ref(user_id),
        tenant_id=str(tenant_id),
        resource_id=str(record.get("id") or ""),
    )


def _gout_fhir(record: dict[str, Any], tenant_id: UUID, user_id: UUID) -> dict[str, Any]:
    return gout_flare_to_observation(
        record,
        patient_ref=_patient_ref(user_id),
        tenant_id=str(tenant_id),
        resource_id=str(record.get("id") or ""),
    )


class PostgresHealthAdapter:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self._session_factory = session_factory or async_session_factory

    @asynccontextmanager
    async def _tx(self, tenant_id: UUID, user_id: UUID) -> AsyncIterator[AsyncSession]:
        async with self._session_factory() as session:
            async with session.begin():
                await set_rls_context(session, tenant_id, user_id)
                yield session

    async def get_profile(self, tenant_id: UUID, user_id: UUID) -> dict[str, Any] | None:
        async with self._tx(tenant_id, user_id) as session:
            result = await session.execute(
                select(PatientProfile).where(
                    PatientProfile.tenant_id == tenant_id,
                    PatientProfile.user_id == user_id,
                )
            )
            row = result.scalar_one_or_none()
            return dict(row.payload) if row else None

    async def upsert_profile(
        self, tenant_id: UUID, user_id: UUID, profile: dict[str, Any]
    ) -> dict[str, Any]:
        async with self._tx(tenant_id, user_id) as session:
            result = await session.execute(
                select(PatientProfile).where(
                    PatientProfile.tenant_id == tenant_id,
                    PatientProfile.user_id == user_id,
                )
            )
            row = result.scalar_one_or_none()
            cols = _profile_columns(profile)
            if row is None:
                payload = _json_safe({**profile, "last_updated": datetime.now(UTC).isoformat()})
                row = PatientProfile(
                    tenant_id=tenant_id,
                    user_id=user_id,
                    payload=payload,
                    fhir=_profile_fhir(payload, tenant_id, user_id),
                    **cols,
                )
                session.add(row)
            else:
                payload = _json_safe({
                    **dict(row.payload or {}),
                    **profile,
                    "last_updated": datetime.now(UTC).isoformat(),
                })
                row.payload = payload
                row.fhir = _profile_fhir(payload, tenant_id, user_id)
                for key, value in cols.items():
                    setattr(row, key, value)
            await session.flush()
            return dict(row.payload)

    async def list_allergies(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]:
        async with self._tx(tenant_id, user_id) as session:
            stmt = select(AllergyRecord).where(
                AllergyRecord.tenant_id == tenant_id,
                AllergyRecord.user_id == user_id,
            )
            if status:
                stmt = stmt.where(AllergyRecord.status == status)
            result = await session.execute(stmt)
            return [dict(row.payload) for row in result.scalars().all()]

    async def add_allergy(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]:
        async with self._tx(tenant_id, user_id) as session:
            record_id = str(record.get("id") or f"allergy_{uuid4().hex[:16]}")
            record = _json_safe({**record, "id": record_id})
            cols = _allergy_columns(record)
            row = AllergyRecord(
                tenant_id=tenant_id,
                user_id=user_id,
                record_id=record_id,
                payload=record,
                fhir=_allergy_fhir(record, tenant_id, user_id),
                **cols,
            )
            session.add(row)
            await session.flush()
            return dict(row.payload)

    async def update_allergy(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None:
        async with self._tx(tenant_id, user_id) as session:
            result = await session.execute(
                select(AllergyRecord).where(
                    AllergyRecord.tenant_id == tenant_id,
                    AllergyRecord.user_id == user_id,
                    AllergyRecord.record_id == record_id,
                )
            )
            row = result.scalar_one_or_none()
            if row is None:
                return None
            payload = _json_safe({**dict(row.payload or {}), **patch, "id": record_id})
            row.payload = payload
            row.fhir = _allergy_fhir(payload, tenant_id, user_id)
            for key, value in _allergy_columns(payload).items():
                setattr(row, key, value)
            await session.flush()
            return dict(row.payload)

    async def delete_allergy(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool:
        async with self._tx(tenant_id, user_id) as session:
            result = await session.execute(
                select(AllergyRecord).where(
                    AllergyRecord.tenant_id == tenant_id,
                    AllergyRecord.user_id == user_id,
                    AllergyRecord.record_id == record_id,
                )
            )
            row = result.scalar_one_or_none()
            if row is None:
                return False
            await session.delete(row)
            return True

    async def list_gout_flares(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]:
        async with self._tx(tenant_id, user_id) as session:
            stmt = select(GoutFlare).where(
                GoutFlare.tenant_id == tenant_id,
                GoutFlare.user_id == user_id,
            )
            if status:
                stmt = stmt.where(GoutFlare.status == status)
            result = await session.execute(stmt)
            return [dict(row.payload) for row in result.scalars().all()]

    async def add_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]:
        async with self._tx(tenant_id, user_id) as session:
            record_id = str(record.get("id") or f"gout-{uuid4().hex[:12]}")
            record = _json_safe({**record, "id": record_id})
            cols = _gout_columns(record)
            row = GoutFlare(
                tenant_id=tenant_id,
                user_id=user_id,
                record_id=record_id,
                payload=record,
                fhir=_gout_fhir(record, tenant_id, user_id),
                **cols,
            )
            session.add(row)
            await session.flush()
            return dict(row.payload)

    async def update_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None:
        async with self._tx(tenant_id, user_id) as session:
            result = await session.execute(
                select(GoutFlare).where(
                    GoutFlare.tenant_id == tenant_id,
                    GoutFlare.user_id == user_id,
                    GoutFlare.record_id == record_id,
                )
            )
            row = result.scalar_one_or_none()
            if row is None:
                return None
            payload = _json_safe({**dict(row.payload or {}), **patch, "id": record_id})
            row.payload = payload
            row.fhir = _gout_fhir(payload, tenant_id, user_id)
            for key, value in _gout_columns(payload).items():
                setattr(row, key, value)
            await session.flush()
            return dict(row.payload)

    async def delete_gout_flare(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool:
        async with self._tx(tenant_id, user_id) as session:
            result = await session.execute(
                select(GoutFlare).where(
                    GoutFlare.tenant_id == tenant_id,
                    GoutFlare.user_id == user_id,
                    GoutFlare.record_id == record_id,
                )
            )
            row = result.scalar_one_or_none()
            if row is None:
                return False
            await session.delete(row)
            return True
