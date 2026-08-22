"""PR-048: add invoice domain

Revision ID: pr048invoice
Revises: pr047dunning
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "pr048invoice"
down_revision: Union[str, Sequence[str], None] = "pr047dunning"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "invoices",
        sa.Column(
            "id",
            sa.Uuid(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "invoice_number",
            sa.String(length=50),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "organisation_id",
            sa.Uuid(),
            sa.ForeignKey(
                "organisations.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "customer_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "subscription_id",
            sa.Uuid(),
            sa.ForeignKey(
                "subscriptions.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "billing_record_id",
            sa.Uuid(),
            sa.ForeignKey(
                "billing_records.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "billing_period_start",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "billing_period_end",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "subtotal",
            sa.Numeric(12, 2),
            nullable=False,
        ),
        sa.Column(
            "tax",
            sa.Numeric(12, 2),
            nullable=False,
        ),
        sa.Column(
            "total",
            sa.Numeric(12, 2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "payment_reference",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "due_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_invoices_organisation_id",
        "invoices",
        ["organisation_id"],
    )
    op.create_index(
        "ix_invoices_customer_id",
        "invoices",
        ["customer_id"],
    )
    op.create_index(
        "ix_invoices_subscription_id",
        "invoices",
        ["subscription_id"],
    )
    op.create_index(
        "ix_invoices_billing_record_id",
        "invoices",
        ["billing_record_id"],
    )
    op.create_index(
        "ix_invoices_status",
        "invoices",
        ["status"],
    )
    op.create_index(
        "ix_invoices_due_at",
        "invoices",
        ["due_at"],
    )

    op.create_table(
        "invoice_line_items",
        sa.Column(
            "id",
            sa.Uuid(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "invoice_id",
            sa.Uuid(),
            sa.ForeignKey(
                "invoices.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Numeric(12, 4),
            nullable=False,
        ),
        sa.Column(
            "unit_amount",
            sa.Numeric(12, 2),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.Numeric(12, 2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_invoice_line_items_invoice_id",
        "invoice_line_items",
        ["invoice_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_invoice_line_items_invoice_id",
        table_name="invoice_line_items",
    )
    op.drop_table("invoice_line_items")

    op.drop_index(
        "ix_invoices_due_at",
        table_name="invoices",
    )
    op.drop_index(
        "ix_invoices_status",
        table_name="invoices",
    )
    op.drop_index(
        "ix_invoices_billing_record_id",
        table_name="invoices",
    )
    op.drop_index(
        "ix_invoices_subscription_id",
        table_name="invoices",
    )
    op.drop_index(
        "ix_invoices_customer_id",
        table_name="invoices",
    )
    op.drop_index(
        "ix_invoices_organisation_id",
        table_name="invoices",
    )
    op.drop_table("invoices")
