# migrations/versions/0236208c74a6_increase_image_url_length.py
"""Increase image_url length

Revision ID: 0236208c74a6
Revises: 3bdad9e08558
Create Date: 2025-04-12 07:22:40.468383
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0236208c74a6'
down_revision = '3bdad9e08558'
branch_labels = None
depends_on = None

def table_exists(connection, table_name):
    """Check if a table exists in the database."""
    inspector = inspect(connection)
    return table_name in inspector.get_table_names()

def upgrade() -> None:
    # Get the connection
    connection = op.get_bind()
    
    # Safely alter column if table exists
    if table_exists(connection, 'courses'):
        op.alter_column('courses', 'image_url',
                   existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
                   type_=sa.String(length=2048),
                   existing_nullable=True)

def downgrade() -> None:
    # Get the connection
    connection = op.get_bind()
    
    # Safely revert column if table exists
    if table_exists(connection, 'courses'):
        op.alter_column('courses', 'image_url',
                   existing_type=sa.String(length=2048),
                   type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
                   existing_nullable=True)