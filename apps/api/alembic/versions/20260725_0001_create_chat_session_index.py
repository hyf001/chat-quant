from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260725_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("sdk_session_id", sa.String(length=128), nullable=True),
        sa.Column("sdk_project_key", sa.String(length=256), nullable=True),
        sa.Column("snippet", sa.String(length=500), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("task_type", sa.String(length=32), nullable=True),
        sa.Column("symbols", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("markets", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("tags", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("current_strategy_version_id", sa.String(length=40), nullable=True),
        sa.Column("current_backtest_run_id", sa.String(length=40), nullable=True),
        sa.Column("data_scope_label", sa.String(length=120), nullable=True),
        sa.Column("last_saved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_chat_sessions_user_updated", "chat_sessions", ["user_id", "updated_at"])
    op.create_index("idx_chat_sessions_sdk", "chat_sessions", ["sdk_session_id"])
    op.create_index("idx_chat_sessions_kind", "chat_sessions", ["kind"])

    op.create_table(
        "chat_session_asset_links",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("chat_session_id", sa.String(length=64), nullable=False),
        sa.Column("asset_type", sa.String(length=40), nullable=False),
        sa.Column("asset_id", sa.String(length=64), nullable=False),
        sa.Column("relation_type", sa.String(length=40), nullable=False),
        sa.Column("sdk_session_id", sa.String(length=128), nullable=True),
        sa.Column("sdk_message_uuid", sa.String(length=128), nullable=True),
        sa.Column("sdk_tool_use_id", sa.String(length=128), nullable=True),
        sa.Column("display_snapshot", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "chat_session_id",
            "asset_type",
            "asset_id",
            "relation_type",
            name="uq_chat_session_asset_link",
        ),
    )
    op.create_index(
        "idx_chat_session_asset_links_session",
        "chat_session_asset_links",
        ["chat_session_id", "created_at"],
    )
    op.create_index(
        "idx_chat_session_asset_links_sdk_message",
        "chat_session_asset_links",
        ["sdk_session_id", "sdk_message_uuid"],
    )


def downgrade() -> None:
    op.drop_index("idx_chat_session_asset_links_sdk_message", "chat_session_asset_links")
    op.drop_index("idx_chat_session_asset_links_session", "chat_session_asset_links")
    op.drop_table("chat_session_asset_links")

    op.drop_index("idx_chat_sessions_kind", "chat_sessions")
    op.drop_index("idx_chat_sessions_sdk", "chat_sessions")
    op.drop_index("idx_chat_sessions_user_updated", "chat_sessions")
    op.drop_table("chat_sessions")
