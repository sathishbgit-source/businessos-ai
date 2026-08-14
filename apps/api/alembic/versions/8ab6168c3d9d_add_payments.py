"""add payments

Revision ID: 8ab6168c3d9d
Revises: 994f210b1b42
Create Date: 2026-08-15 00:17:18.853606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8ab6168c3d9d"
down_revision: Union[str, Sequence[str], None] = "994f210b1b42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create payments table."""

    op.create_table(
        "payments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("organisation_id", sa.UUID(), nullable=False),
        sa.Column("billing_record_id", sa.UUID(), nullable=False),
        sa.Column("subscription_id", sa.UUID(), nullable=False),
        sa.Column("customer_id", sa.UUID(), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column(
            "provider_payment_id",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "failure_reason",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "paid_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["billing_record_id"],
            ["billing_records.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisations.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["subscription_id"],
            ["subscriptions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_payments_organisation_id",
        "payments",
        ["organisation_id"],
    )
    op.create_index(
        "ix_payments_billing_record_id",
        "payments",
        ["billing_record_id"],
    )
    op.create_index(
        "ix_payments_subscription_id",
        "payments",
        ["subscription_id"],
    )
    op.create_index(
        "ix_payments_customer_id",
        "payments",
        ["customer_id"],
    )
    op.create_index(
        "ix_payments_status",
        "payments",
        ["status"],
    )
    op.create_index(
        "ix_payments_provider_payment_id",
        "payments",
        ["provider_payment_id"],
    )


def downgrade() -> None:
    """Drop payments table."""

    op.drop_index(
        "ix_payments_provider_payment_id",
        table_name="payments",
    )
    op.drop_index(
        "ix_payments_status",
        table_name="payments",
    )
    op.drop_index(
        "ix_payments_customer_id",
        table_name="payments",
    )
    op.drop_index(
        "ix_payments_subscription_id",
        table_name="payments",
    )
    op.drop_index(
        "ix_payments_billing_record_id",
        table_name="payments",
    )
    op.drop_index(
        "ix_payments_organisation_id",
        table_name="payments",
    )
    op.drop_table("payments")
