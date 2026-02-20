"""Add all tables

Revision ID: a1e252734537
Revises: 
Create Date: 2026-02-15 00:33:31.841167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1e252734537'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(200), nullable=True),
        sa.Column('username', sa.String(45), nullable=True),
        sa.Column('first_name', sa.String(45), nullable=True),
        sa.Column('last_name', sa.String(45), nullable=True),
        sa.Column('hashed_password', sa.String(200), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=True)
    )
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=True),
        sa.Column('description', sa.String(200), nullable=True),
        sa.Column('priority', sa.Integer, nullable=True),
        sa.Column('status', sa.String(200), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
        sa.Column('task_id', sa.Integer, nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['users.id'])
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
