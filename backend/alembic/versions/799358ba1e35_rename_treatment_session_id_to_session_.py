"""rename_treatment_session_id_to_session_id

Revision ID: 799358ba1e35
Revises: 68675f0d6ca9
Create Date: 2025-11-12 22:23:11.941330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799358ba1e35'
down_revision = '68675f0d6ca9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # This migration was already applied in 68675f0d6ca9
    # Column was already renamed from treatment_session_id to session_id
    # No changes needed - this is a no-op migration
    pass


def downgrade() -> None:
    # This migration was already applied in 68675f0d6ca9
    # No changes needed - this is a no-op migration
    pass

