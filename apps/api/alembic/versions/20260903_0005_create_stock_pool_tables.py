"""Create stock pool tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260903_0005"
down_revision = "20260821_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stock_pools",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("project_id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("project_id", "name", name="uq_stock_pools_project_name"),
    )
    op.create_index(
        "idx_stock_pools_project_updated",
        "stock_pools",
        ["project_id", "updated_at"],
    )

    op.create_table(
        "stock_pool_stocks",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("pool_id", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("tags_json", sa.JSON(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["pool_id"], ["stock_pools.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("pool_id", "symbol", name="uq_stock_pool_stocks_pool_symbol"),
    )
    op.create_index("idx_stock_pool_stocks_pool", "stock_pool_stocks", ["pool_id"])
    op.create_index("idx_stock_pool_stocks_symbol", "stock_pool_stocks", ["symbol"])


def downgrade() -> None:
    op.drop_index("idx_stock_pool_stocks_symbol", table_name="stock_pool_stocks")
    op.drop_index("idx_stock_pool_stocks_pool", table_name="stock_pool_stocks")
    op.drop_table("stock_pool_stocks")
    op.drop_index("idx_stock_pools_project_updated", table_name="stock_pools")
    op.drop_table("stock_pools")
