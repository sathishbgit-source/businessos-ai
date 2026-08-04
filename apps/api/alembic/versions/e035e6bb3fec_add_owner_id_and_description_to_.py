"""add owner_id and description to organisations

Revision ID: e035e6bb3fec
Revises: c48b827d6679
Create Date: 2026-08-04

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e035e6bb3fec"
down_revision: Union[str, Sequence[str], None] = "c48b827d6679"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "organisations",
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "organisations",
        sa.Column(
            "owner_id",
            sa.Uuid(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_organisation_owner",
        "organisations",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_organisation_owner",
        "organisations",
        type_="foreignkey",
    )

    op.drop_column(
        "organisations",
        "owner_id",
    )

    op.drop_column(
        "organisations",
        "description",
    )