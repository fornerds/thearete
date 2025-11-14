"""Add thumbnail metadata columns to uploaded_image

Revision ID: c4d3be2c4a8e
Revises: f6e2737481ae
Create Date: 2025-11-14 16:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c4d3be2c4a8e"
down_revision = "f6e2737481ae"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "uploaded_image",
        sa.Column("thumbnail_storage_path", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "uploaded_image",
        sa.Column("thumbnail_url", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "uploaded_image",
        sa.Column("thumbnail_size", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("uploaded_image", "thumbnail_size")
    op.drop_column("uploaded_image", "thumbnail_url")
    op.drop_column("uploaded_image", "thumbnail_storage_path")

