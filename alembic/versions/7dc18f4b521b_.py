"""empty message

Revision ID: 7dc18f4b521b
Revises: 22b562bad7c4
Create Date: 2025-12-01 04:49:33.625649

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7dc18f4b521b"
down_revision: Union[str, Sequence[str], None] = "22b562bad7c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
