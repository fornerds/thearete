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
    # Rename column from treatment_session_id to session_id
    op.alter_column(
        'treatment_session_image',
        'treatment_session_id',
        new_column_name='session_id',
        existing_type=sa.BigInteger(),
        nullable=False
    )
    
    # Drop old unique constraint
    op.drop_constraint(
        'uq_treatment_session_image_sequence',
        'treatment_session_image',
        type_='unique'
    )
    
    # Create new unique constraint with session_id
    op.create_unique_constraint(
        'uq_treatment_session_image_sequence',
        'treatment_session_image',
        ['session_id', 'sequence_no']
    )
    
    # Rename foreign key constraint
    op.drop_constraint(
        'fk_treatment_session_image_treatment_session_id_treatment_session',
        'treatment_session_image',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'fk_treatment_session_image_session_id_treatment_session',
        'treatment_session_image',
        'treatment_session',
        ['session_id'],
        ['id']
    )


def downgrade() -> None:
    # Rename column back from session_id to treatment_session_id
    op.alter_column(
        'treatment_session_image',
        'session_id',
        new_column_name='treatment_session_id',
        existing_type=sa.BigInteger(),
        nullable=False
    )
    
    # Drop new unique constraint
    op.drop_constraint(
        'uq_treatment_session_image_sequence',
        'treatment_session_image',
        type_='unique'
    )
    
    # Create old unique constraint with treatment_session_id
    op.create_unique_constraint(
        'uq_treatment_session_image_sequence',
        'treatment_session_image',
        ['treatment_session_id', 'sequence_no']
    )
    
    # Rename foreign key constraint back
    op.drop_constraint(
        'fk_treatment_session_image_session_id_treatment_session',
        'treatment_session_image',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'fk_treatment_session_image_treatment_session_id_treatment_session',
        'treatment_session_image',
        'treatment_session',
        ['treatment_session_id'],
        ['id']
    )

