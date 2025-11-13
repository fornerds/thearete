"""add treatment name column

Revision ID: 03486deed5aa
Revises: b62450aa6630
Create Date: 2025-11-09 20:46:09.758273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03486deed5aa'
down_revision = 'b62450aa6630'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("treatment", sa.Column("name", sa.String(length=255), nullable=True))
    

def downgrade() -> None:
    op.drop_column("treatment", "name")


