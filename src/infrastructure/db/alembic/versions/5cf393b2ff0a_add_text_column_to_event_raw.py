"""Add text column to event_raw

Revision ID: 5cf393b2ff0a
Revises: fcd7986fcea4
Create Date: 2026-01-10 12:18:51.069499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cf393b2ff0a'
down_revision: Union[str, Sequence[str], None] = 'fcd7986fcea4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'event_raw',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('session_uid', sa.String(36), index=True),
        sa.Column('timestamp', sa.Integer()),
        sa.Column('app_name', sa.String(100), index=True),
        sa.Column('window_title', sa.String(255)),
        sa.Column('duration', sa.Integer(), index=True),
        sa.Column('entry', sa.Text()),
        sa.Column('is_consulted', sa.Boolean(), index=True, default=False),
        sa.Column('is_written', sa.Boolean(), index=True, default=False),
        sa.Column('created_at', sa.DateTime(), index=True),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('event_raw')

