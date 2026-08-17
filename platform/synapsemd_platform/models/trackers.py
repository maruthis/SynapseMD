"""Tracker schema package — Phase A slice: allergies + gout flares."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, DateTime, Float, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from synapsemd_platform.core.database import Base


class AllergyRecord(Base):
    __tablename__ = "allergies"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "user_id", "record_id", name="uq_allergies_tenant_user_record"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    record_id: Mapped[str] = mapped_column(String(128), nullable=False)
    allergen_name: Mapped[str] = mapped_column(String(255), nullable=False)
    allergen_type: Mapped[str] = mapped_column(String(64), default="other")
    severity: Mapped[str] = mapped_column(String(32), default="unknown")
    status: Mapped[str] = mapped_column(String(32), default="active")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    fhir: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class GoutFlare(Base):
    __tablename__ = "gout_flares"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "user_id", "record_id", name="uq_gout_flares_tenant_user_record"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    record_id: Mapped[str] = mapped_column(String(128), nullable=False)
    onset: Mapped[date | None] = mapped_column(Date, nullable=True)
    joint: Mapped[str | None] = mapped_column(String(128), nullable=True)
    side: Mapped[str | None] = mapped_column(String(32), nullable=True)
    severity: Mapped[str] = mapped_column(String(32), default="unknown")
    status: Mapped[str] = mapped_column(String(32), default="active")
    uric_acid_mg_dl: Mapped[float | None] = mapped_column(Float, nullable=True)
    triggers: Mapped[list[Any]] = mapped_column(JSON, default=list)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    fhir: Mapped[dict] = mapped_column(JSON, default=dict)
    recorded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
