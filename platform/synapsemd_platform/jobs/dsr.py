"""Data-subject request jobs: access, erase, correct, and PHI-free certificates."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.anonymization.engine import AnonymizationEngine
from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.rls import set_rls_context
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore
from synapsemd_platform.models.audit import AIInteraction
from synapsemd_platform.models.clinical import PatientProfile
from synapsemd_platform.models.governance import Consent, DsrRequest, LegalHold
from synapsemd_platform.models.iam import Identity, Session
from synapsemd_platform.models.models_catalog import RoutingDecisionLog
from synapsemd_platform.models.objects import StoredObject
from synapsemd_platform.models.review import ReviewQueueItem
from synapsemd_platform.models.tenant import User
from synapsemd_platform.models.trackers import AllergyRecord, GoutFlare
from synapsemd_platform.storage.object_store import ObjectStore, get_object_store

DSR_TYPES = frozenset({"access", "erase", "correct"})


class LegalHoldActive(Exception):
    def __init__(self, reason: str = "legal_hold") -> None:
        super().__init__(reason)
        self.reason = reason


def object_prefix(tenant_id: UUID, user_id: UUID) -> str:
    return f"objects/{tenant_id}/{user_id}/"


async def legal_hold_active(
    session: AsyncSession,
    tenant_id: UUID,
    user_id: UUID | None = None,
) -> bool:
    if get_settings().audit_legal_hold:
        return True
    stmt = select(LegalHold).where(
        LegalHold.tenant_id == tenant_id,
        LegalHold.active.is_(True),
    )
    if user_id is not None:
        stmt = stmt.where(or_(LegalHold.user_id.is_(None), LegalHold.user_id == user_id))
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


def completion_certificate(
    *,
    request_id: UUID,
    tenant_id: UUID,
    subject_user_id: UUID,
    request_type: str,
    rows_removed: dict[str, int],
    objects_removed: int,
    tokens_removed: int,
    fhir_deleted: bool,
    status: str = "completed",
) -> dict[str, Any]:
    """Certificate of completion — identifiers and counts only, never PHI."""
    return {
        "certificate_id": str(uuid4()),
        "request_id": str(request_id),
        "tenant_id": str(tenant_id),
        "subject_user_id": str(subject_user_id),
        "request_type": request_type,
        "status": status,
        "completed_at": datetime.now(UTC).isoformat(),
        "rows_removed": rows_removed,
        "objects_removed": objects_removed,
        "tokens_removed": tokens_removed,
        "fhir_deleted": fhir_deleted,
        "schema": "synapsemd.dsr.certificate.v1",
    }


async def process_dsr(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    subject_user_id: UUID,
    requested_by: UUID,
    request_type: str,
    correction_payload: dict[str, Any] | None = None,
    store: ObjectStore | None = None,
) -> DsrRequest:
    if request_type not in DSR_TYPES:
        raise ValueError(f"Unknown DSR type: {request_type}")

    row = DsrRequest(
        tenant_id=tenant_id,
        subject_user_id=subject_user_id,
        requested_by=requested_by,
        request_type=request_type,
        status="open",
        correction_payload=correction_payload or {},
    )
    session.add(row)
    await session.flush()

    try:
        if request_type == "access":
            export = await _access(session, tenant_id, subject_user_id)
            cert = completion_certificate(
                request_id=row.id,
                tenant_id=tenant_id,
                subject_user_id=subject_user_id,
                request_type=request_type,
                rows_removed={"exported_resource_count": export["resource_count"]},
                objects_removed=0,
                tokens_removed=0,
                fhir_deleted=False,
            )
            row.certificate = cert
            row.status = "completed"
            row.completed_at = datetime.now(UTC)
            await session.commit()
            await _audit(tenant_id, requested_by, row, "success")
            row.export_payload = export
            return row

        if request_type == "correct":
            counts = await _correct(session, tenant_id, subject_user_id, correction_payload or {})
            cert = completion_certificate(
                request_id=row.id,
                tenant_id=tenant_id,
                subject_user_id=subject_user_id,
                request_type=request_type,
                rows_removed=counts,
                objects_removed=0,
                tokens_removed=0,
                fhir_deleted=False,
            )
            row.certificate = cert
            row.status = "completed"
            row.completed_at = datetime.now(UTC)
            await session.commit()
            await _audit(tenant_id, requested_by, row, "success")
            return row

        if await legal_hold_active(session, tenant_id, subject_user_id):
            raise LegalHoldActive()

        counts = await erase_subject(
            session,
            tenant_id=tenant_id,
            subject_user_id=subject_user_id,
            store=store or get_object_store(),
        )
        cert = completion_certificate(
            request_id=row.id,
            tenant_id=tenant_id,
            subject_user_id=subject_user_id,
            request_type="erase",
            rows_removed=counts["rows_removed"],
            objects_removed=counts["objects_removed"],
            tokens_removed=counts["tokens_removed"],
            fhir_deleted=counts["fhir_deleted"],
        )
        row.certificate = cert
        row.status = "completed"
        row.completed_at = datetime.now(UTC)
        await session.commit()
        await _audit(tenant_id, requested_by, row, "success")
        return row
    except LegalHoldActive:
        row.status = "held"
        row.certificate = completion_certificate(
            request_id=row.id,
            tenant_id=tenant_id,
            subject_user_id=subject_user_id,
            request_type=request_type,
            rows_removed={},
            objects_removed=0,
            tokens_removed=0,
            fhir_deleted=False,
            status="held",
        )
        await session.commit()
        await _audit(tenant_id, requested_by, row, "held")
        raise


async def erase_subject(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    subject_user_id: UUID,
    store: ObjectStore | None = None,
) -> dict[str, Any]:
    """Remove clinical rows, FHIR, object prefix, and token maps. Audit rows stay."""
    await set_rls_context(session, tenant_id, subject_user_id)
    rows_removed: dict[str, int] = {}
    for model, name in (
        (PatientProfile, "patient_profiles"),
        (AllergyRecord, "allergies"),
        (GoutFlare, "gout_flares"),
        (AIInteraction, "ai_interactions"),
        (ReviewQueueItem, "review_queue"),
        (Consent, "consents"),
        (RoutingDecisionLog, "routing_decisions_log"),
        (Identity, "identities"),
        (Session, "sessions"),
        (StoredObject, "stored_objects"),
    ):
        result = await session.execute(
            delete(model).where(model.tenant_id == tenant_id, model.user_id == subject_user_id)
        )
        rows_removed[name] = int(result.rowcount or 0)

    user_result = await session.execute(
        select(User).where(User.id == subject_user_id, User.tenant_id == tenant_id)
    )
    user = user_result.scalar_one_or_none()
    if user is not None:
        user.role = "erased"
        user.password_hash = None
        user.email_hash = f"erased:{subject_user_id}"
        rows_removed["users"] = 1
    else:
        rows_removed["users"] = 0

    store = store or get_object_store()
    objects_removed = store.delete_prefix(object_prefix(tenant_id, subject_user_id))
    tokens_removed = _delete_tokens(str(subject_user_id), str(tenant_id))
    fhir_store = FHIRLocalStore(get_settings().fhir_local_store)
    fhir_deleted = await DataAccessLayer(fhir_store).delete_patient_resources(
        tenant_id, subject_user_id
    )
    _purge_rag(str(tenant_id), str(subject_user_id))
    return {
        "rows_removed": rows_removed,
        "objects_removed": objects_removed,
        "tokens_removed": tokens_removed,
        "fhir_deleted": bool(fhir_deleted),
    }


async def _access(session: AsyncSession, tenant_id: UUID, user_id: UUID) -> dict[str, Any]:
    await set_rls_context(session, tenant_id, user_id)
    profile = await session.execute(
        select(PatientProfile).where(
            PatientProfile.tenant_id == tenant_id, PatientProfile.user_id == user_id
        )
    )
    allergies = await session.execute(
        select(AllergyRecord).where(
            AllergyRecord.tenant_id == tenant_id, AllergyRecord.user_id == user_id
        )
    )
    flares = await session.execute(
        select(GoutFlare).where(GoutFlare.tenant_id == tenant_id, GoutFlare.user_id == user_id)
    )
    dal = DataAccessLayer(FHIRLocalStore(get_settings().fhir_local_store))
    fhir = await dal.get_patient_resources(tenant_id, user_id)
    return {
        "resource_count": len(fhir),
        "profile_present": profile.scalar_one_or_none() is not None,
        "allergy_count": len(allergies.scalars().all()),
        "gout_flare_count": len(flares.scalars().all()),
        "resources": fhir,
    }


async def _correct(
    session: AsyncSession,
    tenant_id: UUID,
    user_id: UUID,
    payload: dict[str, Any],
) -> dict[str, int]:
    await set_rls_context(session, tenant_id, user_id)
    profile_patch = payload.get("profile")
    if not isinstance(profile_patch, dict) or not profile_patch:
        return {"patient_profiles": 0}
    result = await session.execute(
        select(PatientProfile).where(
            PatientProfile.tenant_id == tenant_id, PatientProfile.user_id == user_id
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        return {"patient_profiles": 0}
    merged = {**(row.payload or {}), **profile_patch}
    row.payload = merged
    return {"patient_profiles": 1}


def _delete_tokens(user_id: str, tenant_id: str) -> int:
    vault = AnonymizationEngine().vault
    delete_fn = getattr(vault, "delete_tokens", None)
    if delete_fn is None:
        return 0
    return int(delete_fn(user_id, tenant_id=tenant_id) or 0)


def _purge_rag(tenant_id: str, user_id: str) -> None:
    from synapsemd_platform.rag.retrieval import get_rag_engine

    engine = get_rag_engine()
    purge = getattr(engine, "purge_user_docs", None)
    if purge is not None:
        purge(tenant_id, user_id)


async def _audit(tenant_id: UUID, actor_id: UUID, row: DsrRequest, outcome: str) -> None:
    await audit_producer.emit(
        AuditEventPayload(
            event_type=f"privacy.dsr.{row.request_type}",
            tenant_id=str(tenant_id),
            user_id=str(actor_id),
            resource={
                "request_id": str(row.id),
                "subject_user_id": str(row.subject_user_id),
                "status": row.status,
            },
            outcome=outcome,
        )
    )


async def set_legal_hold(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    created_by: UUID,
    reason: str,
    user_id: UUID | None = None,
    active: bool = True,
) -> LegalHold:
    if active:
        hold = LegalHold(
            tenant_id=tenant_id,
            user_id=user_id,
            active=True,
            reason=reason,
            created_by=created_by,
        )
        session.add(hold)
        await session.commit()
        await session.refresh(hold)
        return hold
    stmt = (
        update(LegalHold)
        .where(
            LegalHold.tenant_id == tenant_id,
            LegalHold.active.is_(True),
        )
        .values(active=False, released_at=datetime.now(UTC))
    )
    if user_id is not None:
        stmt = stmt.where(LegalHold.user_id == user_id)
    else:
        stmt = stmt.where(LegalHold.user_id.is_(None))
    await session.execute(stmt)
    await session.commit()
    result = await session.execute(
        select(LegalHold)
        .where(LegalHold.tenant_id == tenant_id)
        .order_by(LegalHold.created_at.desc())
    )
    row = result.scalars().first()
    if row is None:
        row = LegalHold(
            tenant_id=tenant_id,
            user_id=user_id,
            active=False,
            reason=reason,
            created_by=created_by,
            released_at=datetime.now(UTC),
        )
        session.add(row)
        await session.commit()
    return row
