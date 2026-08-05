"""add deleted_at to organisations

Revision ID: 2f84a1d9effa
Revises: e035e6bb3fec
Create Date: 2026-08-05 23:29:13.312324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f84a1d9effa'
down_revision: Union[str, Sequence[str], None] = 'e035e6bb3fec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "organisations",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "organisations",
        "deleted_at",
    )