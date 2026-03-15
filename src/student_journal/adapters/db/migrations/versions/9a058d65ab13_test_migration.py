"""Test migration.

Revision ID: 9a058d65ab13
Revises: 55cf069466d5
Create Date: 2025-09-08 15:27:23.356780

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "9a058d65ab13"
down_revision: str | Sequence[str] | None = "55cf069466d5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
