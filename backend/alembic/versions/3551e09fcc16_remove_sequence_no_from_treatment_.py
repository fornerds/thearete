"""remove_sequence_no_from_treatment_session_image

Revision ID: 3551e09fcc16
Revises: c0c4707ad8b7
Create Date: 2025-11-15 13:09:09.764909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3551e09fcc16'
down_revision = 'c0c4707ad8b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Unique constraint 제거
    op.drop_constraint('uq_treatment_session_image_sequence', 'treatment_session_image', type_='unique')
    # sequence_no 컬럼 제거
    op.drop_column('treatment_session_image', 'sequence_no')

def downgrade() -> None:
    # sequence_no 컬럼 추가
    op.add_column('treatment_session_image', sa.Column('sequence_no', sa.Integer(), nullable=False, server_default='0'))
    # Unique constraint 추가
    op.create_unique_constraint('uq_treatment_session_image_sequence', 'treatment_session_image', ['session_id', 'sequence_no'])