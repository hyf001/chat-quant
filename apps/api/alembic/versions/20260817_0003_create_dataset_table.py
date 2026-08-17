"""Create dataset metadata table."""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260817_0003"
down_revision = "20260726_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "datasets",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category_path_json", sa.JSON(), nullable=False),
        sa.Column("exposed_to_agent", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("name", name="uq_datasets_name"),
    )
    op.create_index("idx_datasets_exposed_updated", "datasets", ["exposed_to_agent", "updated_at"])
    op.create_index("idx_datasets_name", "datasets", ["name"])


def downgrade() -> None:
    op.drop_index("idx_datasets_name", table_name="datasets")
    op.drop_index("idx_datasets_exposed_updated", table_name="datasets")
    op.drop_table("datasets")
