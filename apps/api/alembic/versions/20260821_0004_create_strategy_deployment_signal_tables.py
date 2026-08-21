"""Create strategy deployment and signal tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260821_0004"
down_revision = "20260817_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "strategy_deployments",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("strategy_id", sa.String(length=64), nullable=False),
        sa.Column("strategy_version_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("mode", sa.String(length=32), nullable=False),
        sa.Column("symbols_json", sa.JSON(), nullable=False),
        sa.Column("lookback_bars", sa.Integer(), nullable=False),
        sa.Column("params_json", sa.JSON(), nullable=False),
        sa.Column("broker_id", sa.String(length=128), nullable=True),
        sa.Column("requires_manual_confirm", sa.Boolean(), nullable=False),
        sa.Column("risk_config_json", sa.JSON(), nullable=False),
        sa.Column("state_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["strategy_id"], ["strategies.id"]),
        sa.ForeignKeyConstraint(["strategy_version_id"], ["strategy_versions.id"]),
    )
    op.create_index(
        "idx_strategy_deployments_project_updated",
        "strategy_deployments",
        ["project_id", "updated_at"],
    )
    op.create_index(
        "idx_strategy_deployments_strategy",
        "strategy_deployments",
        ["strategy_id", "strategy_version_id"],
    )
    op.create_index(
        "idx_strategy_deployments_mode",
        "strategy_deployments",
        ["mode"],
    )

    op.create_table(
        "strategy_signals",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("deployment_id", sa.String(length=64), nullable=False),
        sa.Column("job_instance_id", sa.String(length=64), nullable=True),
        sa.Column("strategy_version_id", sa.String(length=64), nullable=False),
        sa.Column("signal_datetime", sa.DateTime(), nullable=False),
        sa.Column("action_json", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["deployment_id"], ["strategy_deployments.id"]),
        sa.ForeignKeyConstraint(["job_instance_id"], ["job_instances.id"]),
        sa.ForeignKeyConstraint(["strategy_version_id"], ["strategy_versions.id"]),
    )
    op.create_index(
        "idx_strategy_signals_deployment_datetime",
        "strategy_signals",
        ["deployment_id", "signal_datetime"],
    )
    op.create_index("idx_strategy_signals_job_instance", "strategy_signals", ["job_instance_id"])
    op.create_index("idx_strategy_signals_status", "strategy_signals", ["status"])


def downgrade() -> None:
    op.drop_index("idx_strategy_signals_status", table_name="strategy_signals")
    op.drop_index("idx_strategy_signals_job_instance", table_name="strategy_signals")
    op.drop_index("idx_strategy_signals_deployment_datetime", table_name="strategy_signals")
    op.drop_table("strategy_signals")
    op.drop_index("idx_strategy_deployments_mode", table_name="strategy_deployments")
    op.drop_index("idx_strategy_deployments_strategy", table_name="strategy_deployments")
    op.drop_index("idx_strategy_deployments_project_updated", table_name="strategy_deployments")
    op.drop_table("strategy_deployments")
