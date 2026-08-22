"""PR-047: add dunning failed-payment management

Revision ID: pr047dunning
Revises: fe8b8a3c3e17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "pr047dunning"
down_revision: Union[str, Sequence[str], None] = "fe8b8a3c3e17"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dunning_records",
        sa.Column(
            "id",
            sa.Uuid(),
            primary_key=True,
            nullable=False,
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
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "next_retry_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "grace_period_ends_at",
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
    )

    op.create_index(
        "ix_dunning_records_organisation_id",
        "dunning_records",
        ["organisation_id"],
    )
    op.create_index(
        "ix_dunning_records_subscription_id",
        "dunning_records",
        ["subscription_id"],
    )
    op.create_index(
        "ix_dunning_records_billing_record_id",
        "dunning_records",
        ["billing_record_id"],
    )
    op.create_index(
        "ix_dunning_records_status",
        "dunning_records",
        ["status"],
    )
    op.create_index(
        "ix_dunning_records_next_retry_at",
        "dunning_records",
        ["next_retry_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_dunning_records_next_retry_at",
        table_name="dunning_records",
    )
    op.drop_index(
        "ix_dunning_records_status",
        table_name="dunning_records",
    )
    op.drop_index(
        "ix_dunning_records_billing_record_id",
        table_name="dunning_records",
    )
    op.drop_index(
        "ix_dunning_records_subscription_id",
        table_name="dunning_records",
    )
    op.drop_index(
        "ix_dunning_records_organisation_id",
        table_name="dunning_records",
    )
    op.drop_table("dunning_records")
