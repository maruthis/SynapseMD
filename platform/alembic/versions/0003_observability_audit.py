"""Observability audit columns, indexes, and append-only trigger.

Revision ID: 0003_observability_audit
Revises: 0002_identity_access
Create Date: 2026-08-17

C-7: Native RANGE partitioning of an existing table requires a rewrite.
This revision stores partition_month and indexes (tenant_id, occurred_at)
so monthly queries work. Attach PostgreSQL monthly partitions in a later
ops change if volume requires it.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from synapsemd_platform.audit.append_only import AUDIT_APPEND_ONLY_STATEMENTS

revision: str = "0003_observability_audit"
down_revision: str | None = "0002_identity_access"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_NEW_COLUMNS = (
    sa.Column("event_id", sa.String(32), nullable=True),
    sa.Column("event_hash", sa.String(128), nullable=True),
    sa.Column("prev_hash", sa.String(128), nullable=True),
    sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("partition_month", sa.String(7), nullable=True),
)

_INDEXES = (
    ("ix_audit_events_event_id", ["event_id"]),
    ("ix_audit_events_occurred_at", ["occurred_at"]),
    ("ix_audit_events_partition_month", ["partition_month"]),
    ("ix_audit_events_tenant_occurred", ["tenant_id", "occurred_at"]),
)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing = {column["name"] for column in inspector.get_columns("audit_events")}
    missing = [column for column in _NEW_COLUMNS if column.name not in existing]
    if missing:
        with op.batch_alter_table("audit_events") as batch:
            for column in missing:
                batch.add_column(column)

    inspector = sa.inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("audit_events")}
    for name, cols in _INDEXES:
        if name not in existing_indexes:
            op.create_index(name, "audit_events", cols)

    if bind.dialect.name == "postgresql":
        for statement in AUDIT_APPEND_ONLY_STATEMENTS:
            op.execute(sa.text(statement))


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(sa.text("DROP TRIGGER IF EXISTS audit_events_no_update ON audit_events"))
        op.execute(sa.text("DROP TRIGGER IF EXISTS audit_events_no_delete ON audit_events"))
        op.execute(sa.text("DROP FUNCTION IF EXISTS audit_events_deny_mutation()"))

    inspector = sa.inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("audit_events")}
    for name, _cols in reversed(_INDEXES):
        if name in existing_indexes:
            op.drop_index(name, table_name="audit_events")

    inspector = sa.inspect(bind)
    existing = {column["name"] for column in inspector.get_columns("audit_events")}
    with op.batch_alter_table("audit_events") as batch:
        for column in reversed(_NEW_COLUMNS):
            if column.name in existing:
                batch.drop_column(column.name)
