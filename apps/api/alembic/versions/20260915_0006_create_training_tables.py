"""Create training tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260915_0006"
down_revision = "20260903_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "training_sessions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("mode", sa.String(length=16), nullable=False),
        sa.Column("period", sa.String(length=8), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("slice_start", sa.Date(), nullable=False),
        sa.Column("slice_end", sa.Date(), nullable=False),
        sa.Column("warmup_bars", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("initial_cash", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("config_json", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "idx_training_sessions_project",
        "training_sessions",
        ["project_id", "created_at"],
    )
    op.create_index("idx_training_sessions_status", "training_sessions", ["status"])

    op.create_table(
        "training_events",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("seq", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("session_id", "seq", name="uq_training_events_session_seq"),
    )
    op.create_index("idx_training_events_session", "training_events", ["session_id", "seq"])


def downgrade() -> None:
    op.drop_index("idx_training_events_session", table_name="training_events")
    op.drop_table("training_events")
    op.drop_index("idx_training_sessions_status", table_name="training_sessions")
    op.drop_index("idx_training_sessions_project", table_name="training_sessions")
    op.drop_table("training_sessions")
