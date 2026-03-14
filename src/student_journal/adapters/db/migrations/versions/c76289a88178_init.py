"""Init.

Revision ID: c76289a88178
Revises:
Create Date: 2025-09-08 12:49:02.837733

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "c76289a88178"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
