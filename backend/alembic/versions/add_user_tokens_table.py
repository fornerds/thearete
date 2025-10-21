"""Add user tokens table for refresh token management

Revision ID: add_user_tokens_table
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_tokens_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add user_tokens table."""
    # Create user_tokens table
    op.create_table(
        'user_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token_hash', sa.String(length=255), nullable=False),
        sa.Column('token_type', sa.String(length=50), nullable=False),
        sa.Column('is_revoked', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.Column('device_info', sa.Text(), nullable=True),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_user_tokens_id'), 'user_tokens', ['id'], unique=False)
    op.create_index(op.f('ix_user_tokens_user_id'), 'user_tokens', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_tokens_token_hash'), 'user_tokens', ['token_hash'], unique=True)
    op.create_index(op.f('ix_user_tokens_expires_at'), 'user_tokens', ['expires_at'], unique=False)
    op.create_index(op.f('ix_user_tokens_session_id'), 'user_tokens', ['session_id'], unique=False)


def downgrade() -> None:
    """Remove user_tokens table."""
    # Drop indexes
    op.drop_index(op.f('ix_user_tokens_session_id'), table_name='user_tokens')
    op.drop_index(op.f('ix_user_tokens_expires_at'), table_name='user_tokens')
    op.drop_index(op.f('ix_user_tokens_token_hash'), table_name='user_tokens')
    op.drop_index(op.f('ix_user_tokens_user_id'), table_name='user_tokens')
    op.drop_index(op.f('ix_user_tokens_id'), table_name='user_tokens')
    
    # Drop table
    op.drop_table('user_tokens')
