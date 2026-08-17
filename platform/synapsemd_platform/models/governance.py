"""Governance schema stubs — Phase A placeholder; consent/purpose land in Phase B."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from synapsemd_platform.core.database import Base

LLM_PROCESSING_PURPOSE = "llm_processing"


class Consent(Base):
    __tablename__ = "consents"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    purpose: Mapped[str] = mapped_column(String(64), nullable=False, default=LLM_PROCESSING_PURPOSE)
    granted: Mapped[bool] = mapped_column(Boolean, default=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="implicit")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BaaRecord(Base):
    """Signed BAA registry used by the model policy engine (D-12)."""

    __tablename__ = "baa_records"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    provider: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    signed: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    environment: Mapped[str] = mapped_column(String(32), nullable=False, default="production")
    signed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DsrRequest(Base):
    """GDPR/HIPAA data-subject request (access / erase / correct)."""

    __tablename__ = "dsr_requests"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    subject_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    requested_by: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    request_type: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")
    correction_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    certificate: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LegalHold(Base):
    """Tenant or per-user hold that blocks purge, erasure, and WORM delete."""

    __tablename__ = "legal_holds"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
