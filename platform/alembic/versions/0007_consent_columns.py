"""Add missing consent columns on existing Postgres volumes.

Revision ID: 0007_consent_columns
Revises: 0006_data_plane_complete
Create Date: 2026-08-17

create_all in earlier revisions does not ALTER existing tables. Local Compose
volumes created before Consent.source / expires_at need this upgrade.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0007_consent_columns"
down_revision: str | None = "0006_data_plane_complete"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "consents" not in inspector.get_table_names():
        return
    columns = {col["name"] for col in inspector.get_columns("consents")}
    if "source" not in columns:
        op.add_column(
            "consents",
            sa.Column("source", sa.String(32), nullable=False, server_default="implicit"),
        )
    if "expires_at" not in columns:
        op.add_column("consents", sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "consents" not in inspector.get_table_names():
        return
    columns = {col["name"] for col in inspector.get_columns("consents")}
    if "expires_at" in columns:
        op.drop_column("consents", "expires_at")
    if "source" in columns:
        op.drop_column("consents", "source")
