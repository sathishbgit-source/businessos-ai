"""add payment provider reference uniqueness

Revision ID: fe8b8a3c3e17
Revises: 8ab6168c3d9d
Create Date: 2026-08-16 00:32:08.294671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fe8b8a3c3e17"
down_revision: Union[str, Sequence[str], None] = "8ab6168c3d9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add provider-scoped payment reference uniqueness."""

    op.create_unique_constraint(
        "uq_payments_provider_provider_payment_id",
        "payments",
        ["provider", "provider_payment_id"],
    )


def downgrade() -> None:
    """Remove provider-scoped payment reference uniqueness."""

    op.drop_constraint(
        "uq_payments_provider_provider_payment_id",
        "payments",
        type_="unique",
    )
