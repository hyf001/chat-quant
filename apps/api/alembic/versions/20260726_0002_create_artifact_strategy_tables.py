from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260726_0002"
down_revision = "20260725_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "code_artifacts",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("chat_session_id", sa.String(length=64), nullable=False),
        sa.Column("source_sdk_session_id", sa.String(length=128), nullable=True),
        sa.Column("source_sdk_message_uuid", sa.String(length=128), nullable=True),
        sa.Column("source_sdk_tool_use_id", sa.String(length=128), nullable=True),
        sa.Column("artifact_type", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("entrypoint", sa.String(length=256), nullable=True),
        sa.Column("root_path", sa.String(length=512), nullable=False),
        sa.Column("main_file_id", sa.String(length=64), nullable=True),
        sa.Column("checksum", sa.String(length=128), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "source_sdk_tool_use_id",
            "artifact_type",
            "checksum",
            "entrypoint",
            name="uq_code_artifacts_idempotent",
        ),
    )
    op.create_index(
        "idx_code_artifacts_chat_created",
        "code_artifacts",
        ["chat_session_id", "created_at"],
    )
    op.create_index("idx_code_artifacts_sdk_tool_use", "code_artifacts", ["source_sdk_tool_use_id"])
    op.create_index("idx_code_artifacts_type", "code_artifacts", ["artifact_type"])

    op.create_table(
        "artifact_files",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("artifact_id", sa.String(length=64), nullable=False),
        sa.Column("file_role", sa.String(length=40), nullable=False),
        sa.Column("relative_path", sa.String(length=512), nullable=False),
        sa.Column("storage_uri", sa.String(length=1024), nullable=False),
        sa.Column("mime_type", sa.String(length=128), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("checksum", sa.String(length=128), nullable=False),
        sa.Column("is_entrypoint", sa.Boolean(), nullable=False),
        sa.Column("render_metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["artifact_id"], ["code_artifacts.id"]),
        sa.UniqueConstraint("artifact_id", "relative_path", name="uq_artifact_files_path"),
    )
    op.create_index("idx_artifact_files_artifact", "artifact_files", ["artifact_id"])
    op.create_index("idx_artifact_files_role", "artifact_files", ["file_role"])

    op.create_table(
        "artifact_versions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("artifact_id", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("root_path", sa.String(length=512), nullable=False),
        sa.Column("checksum", sa.String(length=128), nullable=False),
        sa.Column("entrypoint", sa.String(length=256), nullable=True),
        sa.Column("manifest_json", sa.JSON(), nullable=False),
        sa.Column("created_by_sdk_tool_use_id", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["artifact_id"], ["code_artifacts.id"]),
        sa.UniqueConstraint("artifact_id", "version", name="uq_artifact_versions_version"),
        sa.UniqueConstraint(
            "artifact_id",
            "checksum",
            "entrypoint",
            name="uq_artifact_versions_checksum",
        ),
    )

    op.create_table(
        "artifact_links",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("artifact_id", sa.String(length=64), nullable=False),
        sa.Column("file_id", sa.String(length=64), nullable=True),
        sa.Column("target_type", sa.String(length=40), nullable=False),
        sa.Column("target_id", sa.String(length=128), nullable=False),
        sa.Column("relation", sa.String(length=40), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_artifact_links_target", "artifact_links", ["target_type", "target_id"])
    op.create_index("idx_artifact_links_artifact", "artifact_links", ["artifact_id"])

    op.create_table(
        "strategies",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("chat_session_id", sa.String(length=64), nullable=False),
        sa.Column("source_sdk_message_uuid", sa.String(length=128), nullable=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("strategy_type", sa.String(length=64), nullable=False),
        sa.Column("tags_json", sa.JSON(), nullable=False),
        sa.Column("current_version_id", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
    )
    op.create_index(
        "idx_strategies_user_project_updated",
        "strategies",
        ["user_id", "project_id", "updated_at"],
    )
    op.create_index("idx_strategies_chat_session", "strategies", ["chat_session_id"])
    op.create_index("idx_strategies_type", "strategies", ["strategy_type"])

    op.create_table(
        "strategy_versions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("strategy_id", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("version_name", sa.String(length=128), nullable=True),
        sa.Column("parent_version_id", sa.String(length=64), nullable=True),
        sa.Column("code_artifact_id", sa.String(length=128), nullable=False),
        sa.Column("entrypoint", sa.String(length=256), nullable=False),
        sa.Column("params_schema_json", sa.JSON(), nullable=False),
        sa.Column("default_params_json", sa.JSON(), nullable=False),
        sa.Column("logic_summary", sa.Text(), nullable=True),
        sa.Column("change_summary", sa.Text(), nullable=True),
        sa.Column("source_sdk_session_id", sa.String(length=128), nullable=True),
        sa.Column("source_sdk_message_uuid", sa.String(length=128), nullable=True),
        sa.Column("source_sdk_tool_use_id", sa.String(length=128), nullable=True),
        sa.Column("code_checksum", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["strategy_id"], ["strategies.id"]),
        sa.UniqueConstraint("strategy_id", "version", name="uq_strategy_versions_strategy_version"),
    )
    op.create_index(
        "idx_strategy_versions_strategy",
        "strategy_versions",
        ["strategy_id", "version"],
    )
    op.create_index("idx_strategy_versions_parent", "strategy_versions", ["parent_version_id"])
    op.create_index("idx_strategy_versions_artifact", "strategy_versions", ["code_artifact_id"])
    op.create_index("idx_strategy_versions_status", "strategy_versions", ["status"])

    op.create_table(
        "strategy_backtests",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("chat_session_id", sa.String(length=64), nullable=False),
        sa.Column("strategy_id", sa.String(length=64), nullable=False),
        sa.Column("strategy_version_id", sa.String(length=64), nullable=False),
        sa.Column("run_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("config_hash", sa.String(length=128), nullable=False),
        sa.Column("result_id", sa.String(length=64), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["strategy_id"], ["strategies.id"]),
        sa.ForeignKeyConstraint(["strategy_version_id"], ["strategy_versions.id"]),
    )
    op.create_index(
        "idx_strategy_backtests_version_created",
        "strategy_backtests",
        ["strategy_version_id", "created_at"],
    )
    op.create_index("idx_strategy_backtests_status", "strategy_backtests", ["status"])

    op.create_table(
        "strategy_backtest_results",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("strategy_backtest_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["strategy_backtest_id"], ["strategy_backtests.id"]),
        sa.UniqueConstraint("strategy_backtest_id", name="uq_strategy_backtest_results_run"),
    )


def downgrade() -> None:
    op.drop_table("strategy_backtest_results")
    op.drop_index("idx_strategy_backtests_status", "strategy_backtests")
    op.drop_index("idx_strategy_backtests_version_created", "strategy_backtests")
    op.drop_table("strategy_backtests")
    op.drop_index("idx_strategy_versions_status", "strategy_versions")
    op.drop_index("idx_strategy_versions_artifact", "strategy_versions")
    op.drop_index("idx_strategy_versions_parent", "strategy_versions")
    op.drop_index("idx_strategy_versions_strategy", "strategy_versions")
    op.drop_table("strategy_versions")
    op.drop_index("idx_strategies_type", "strategies")
    op.drop_index("idx_strategies_chat_session", "strategies")
    op.drop_index("idx_strategies_user_project_updated", "strategies")
    op.drop_table("strategies")
    op.drop_index("idx_artifact_links_artifact", "artifact_links")
    op.drop_index("idx_artifact_links_target", "artifact_links")
    op.drop_table("artifact_links")
    op.drop_table("artifact_versions")
    op.drop_index("idx_artifact_files_role", "artifact_files")
    op.drop_index("idx_artifact_files_artifact", "artifact_files")
    op.drop_table("artifact_files")
    op.drop_index("idx_code_artifacts_type", "code_artifacts")
    op.drop_index("idx_code_artifacts_sdk_tool_use", "code_artifacts")
    op.drop_index("idx_code_artifacts_chat_created", "code_artifacts")
    op.drop_table("code_artifacts")
