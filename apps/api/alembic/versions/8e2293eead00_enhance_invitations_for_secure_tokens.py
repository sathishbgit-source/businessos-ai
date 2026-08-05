"""enhance invitations for secure tokens

Revision ID: 8e2293eead00
Revises: 2f84a1d9effa
Create Date: 2026-08-05 23:56:51.520942
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8e2293eead00"
down_revision: Union[str, Sequence[str], None] = "2f84a1d9effa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "invitations",
        sa.Column("token_hash", sa.String(length=64), nullable=False),
    )

    op.add_column(
        "invitations",
        sa.Column("created_by", sa.Uuid(), nullable=True),
    )

    op.add_column(
        "invitations",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )

    op.drop_index(
        op.f("ix_invitations_email"),
        table_name="invitations",
    )

    op.drop_index(
        op.f("ix_invitations_token"),
        table_name="invitations",
    )

    op.create_index(
        "ix_invitation_email",
        "invitations",
        ["email"],
        unique=False,
    )

    op.create_index(
        "ix_invitation_expires_at",
        "invitations",
        ["expires_at"],
        unique=False,
    )

    op.create_index(
        "ix_invitation_organisation_id",
        "invitations",
        ["organisation_id"],
        unique=False,
    )

    op.create_index(
        "ix_invitation_token_hash",
        "invitations",
        ["token_hash"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_invitations_token_hash",
        "invitations",
        ["token_hash"],
    )

    op.create_foreign_key(
        "fk_invitations_created_by_users",
        "invitations",
        "users",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )

    op.drop_column(
        "invitations",
        "token",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        "invitations",
        sa.Column(
            "token",
            sa.String(length=255),
            nullable=False,
        ),
    )

    op.drop_constraint(
        "fk_invitations_created_by_users",
        "invitations",
        type_="foreignkey",
    )

    op.drop_constraint(
        "uq_invitations_token_hash",
        "invitations",
        type_="unique",
    )

    op.drop_index(
        "ix_invitation_token_hash",
        table_name="invitations",
    )

    op.drop_index(
        "ix_invitation_organisation_id",
        table_name="invitations",
    )

    op.drop_index(
        "ix_invitation_expires_at",
        table_name="invitations",
    )

    op.drop_index(
        "ix_invitation_email",
        table_name="invitations",
    )

    op.create_index(
        op.f("ix_invitations_token"),
        "invitations",
        ["token"],
        unique=True,
    )

    op.create_index(
        op.f("ix_invitations_email"),
        "invitations",
        ["email"],
        unique=False,
    )

    op.drop_column(
        "invitations",
        "updated_at",
    )

    op.drop_column(
        "invitations",
        "created_by",
    )

    op.drop_column(
        "invitations",
        "token_hash",
    )