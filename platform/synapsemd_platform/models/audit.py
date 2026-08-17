import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Index, Integer, String, Uuid, event, func
from sqlalchemy.orm import Mapped, mapped_column

from synapsemd_platform.core.database import Base


class AppendOnlyError(RuntimeError):
    pass


class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = (Index("ix_audit_events_tenant_occurred", "tenant_id", "occurred_at"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    signature: Mapped[str | None] = mapped_column(String(128), nullable=True)
    event_id: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    event_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    prev_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    occurred_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    partition_month: Mapped[str | None] = mapped_column(String(7), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


@event.listens_for(AuditEvent, "before_update")
def _deny_audit_update(mapper, connection, target) -> None:  # noqa: ANN001
    raise AppendOnlyError("audit_events is append-only")


@event.listens_for(AuditEvent, "before_delete")
def _deny_audit_delete(mapper, connection, target) -> None:  # noqa: ANN001
    raise AppendOnlyError("audit_events is append-only")


class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    command: Mapped[str] = mapped_column(String(128), nullable=False)
    model_used: Mapped[str] = mapped_column(String(128), nullable=False)
    prompt_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    response_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    reasoning_trace: Mapped[dict] = mapped_column(JSON, default=dict)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    tokens_in: Mapped[int] = mapped_column(Integer, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, default=0)
    safety_flags: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
