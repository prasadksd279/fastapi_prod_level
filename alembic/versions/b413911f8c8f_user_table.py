"""user table

Revision ID: b413911f8c8f
Revises: 7dc18f4b521b
Create Date: 2025-12-01 05:28:40.268783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b413911f8c8f'
down_revision: Union[str, Sequence[str], None] = '7dc18f4b521b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
