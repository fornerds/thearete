"""Add color recipe columns to skin color measurement

Revision ID: c0c4707ad8b7
Revises: 0984d45fd884
Create Date: 2025-11-14 09:08:00.270196

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c0c4707ad8b7'
down_revision = '0984d45fd884'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'skin_color_measurement',
        sa.Column('melanin', sa.Integer(), nullable=True, comment='추론된 멜라닌 투입량 (0~9)')
    )
    op.add_column(
        'skin_color_measurement',
        sa.Column('white', sa.Integer(), nullable=True, comment='추론된 화이트 투입량 (0~9)')
    )
    op.add_column(
        'skin_color_measurement',
        sa.Column('red', sa.Integer(), nullable=True, comment='추론된 레드 투입량 (0~9)')
    )
    op.add_column(
        'skin_color_measurement',
        sa.Column('yellow', sa.Integer(), nullable=True, comment='추론된 옐로우 투입량 (0~9)')
    )


def downgrade() -> None:
    op.drop_column('skin_color_measurement', 'yellow')
    op.drop_column('skin_color_measurement', 'red')
    op.drop_column('skin_color_measurement', 'white')
    op.drop_column('skin_color_measurement', 'melanin')

