"""fix subscription billing plan foreign keys

Revision ID: 994f210b1b42
Revises: 9f983bba3645
Create Date: 2026-08-14 23:06:01.316687

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "994f210b1b42"
down_revision: Union[str, Sequence[str], None] = "9f983bba3645"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add plan foreign keys to subscriptions and billing records."""

    op.create_foreign_key(
        "fk_subscriptions_plan_id_plans",
        "subscriptions",
        "plans",
        ["plan_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.create_foreign_key(
        "fk_billing_records_plan_id_plans",
        "billing_records",
        "plans",
        ["plan_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    """Remove plan foreign keys from subscriptions and billing records."""

    op.drop_constraint(
        "fk_billing_records_plan_id_plans",
        "billing_records",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_subscriptions_plan_id_plans",
        "subscriptions",
        type_="foreignkey",
    )
