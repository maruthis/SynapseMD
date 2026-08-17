"""FHIR projection column, object metadata, command catalog.

Revision ID: 0006_data_plane_complete
Revises: 0005_privacy_ops
Create Date: 2026-08-17
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from synapsemd_platform.core.database import Base
from synapsemd_platform.core.rls import RLS_SQL
from synapsemd_platform.models import (  # noqa: F401
    audit,
    clinical,
    commands,
    governance,
    iam,
    models_catalog,
    objects,
    review,
    tenant,
    trackers,
)
from synapsemd_platform.models.commands import CommandCatalogEntry, command_seed_rows

revision: str = "0006_data_plane_complete"
down_revision: str | None = "0005_privacy_ops"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for table in ("patient_profiles", "allergies", "gout_flares"):
        if table not in inspector.get_table_names():
            continue
        columns = {col["name"] for col in inspector.get_columns(table)}
        if "fhir" not in columns:
            op.add_column(table, sa.Column("fhir", sa.JSON(), nullable=True))
    Base.metadata.create_all(bind)
    existing = {
        row[0] for row in bind.execute(sa.text("SELECT command_id FROM command_catalog")).fetchall()
    }
    rows = [item for item in command_seed_rows() if item["command_id"] not in existing]
    if rows:
        op.bulk_insert(CommandCatalogEntry.__table__, rows)
    if bind.dialect.name == "postgresql":
        op.execute(sa.text(RLS_SQL))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if "stored_objects" in tables:
        op.drop_table("stored_objects")
    if "command_catalog" in tables:
        op.drop_table("command_catalog")
    for table in ("patient_profiles", "allergies", "gout_flares"):
        if table not in tables:
            continue
        columns = {col["name"] for col in inspector.get_columns(table)}
        if "fhir" in columns:
            op.drop_column(table, "fhir")
