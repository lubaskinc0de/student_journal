"""test migration

Revision ID: 9a058d65ab13
Revises: 55cf069466d5
Create Date: 2025-09-08 15:27:23.356780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a058d65ab13'
down_revision: Union[str, Sequence[str], None] = '55cf069466d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
