# migrations/versions/0a21fe616442_add_game_tables.py
"""add_game_tables

Revision ID: 0a21fe616442
Revises: 0236208c74a6
Create Date: 2025-04-12 20:41:47.183225
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '0a21fe616442'
down_revision = '0236208c74a6'
branch_labels = None
depends_on = None

def table_exists(connection, table_name):
    """Check if a table exists in the database."""
    inspector = inspect(connection)
    return table_name in inspector.get_table_names()

def upgrade() -> None:
    # Get the connection
    connection = op.get_bind()
    
    # Create games table if it doesn't exist
    if not table_exists(connection, 'games'):
        op.create_table('games',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('short_description', sa.String(length=255), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('xp_reward', sa.Integer(), nullable=True),
        sa.Column('estimated_time', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
        )
        op.create_index(op.f('ix_games_id'), 'games', ['id'], unique=False)
    
    # Create user_game_progress table if it doesn't exist
    if not table_exists(connection, 'user_game_progress'):
        op.create_table('user_game_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('is_started', sa.Boolean(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=True),
        sa.Column('current_level', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('data', sa.Text(), nullable=True),
        sa.Column('last_played_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'game_id', name='uq_user_game')
        )
        op.create_index(op.f('ix_user_game_progress_id'), 'user_game_progress', ['id'], unique=False)

def downgrade() -> None:
    # Get the connection
    connection = op.get_bind()
    
    # Drop tables only if they exist
    tables_to_drop = [
        ('user_game_progress', 'ix_user_game_progress_id'),
        ('games', 'ix_games_id')
    ]
    
    for table_name, index_name in tables_to_drop:
        if table_exists(connection, table_name):
            op.drop_index(op.f(index_name), table_name=table_name)
            op.drop_table(table_name)