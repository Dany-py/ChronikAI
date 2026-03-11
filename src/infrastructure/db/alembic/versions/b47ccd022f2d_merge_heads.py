"""merge heads

Revision ID: b47ccd022f2d
Revises: 5b4abfa89cec, 781080995749
Create Date: 2026-02-10 08:53:45.784818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b47ccd022f2d'
down_revision: Union[str, Sequence[str], None] = ('5b4abfa89cec', '781080995749')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
