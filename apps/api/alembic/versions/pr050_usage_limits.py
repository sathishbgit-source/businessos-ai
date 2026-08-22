"""PR-050 usage limits.

Revision ID: pr050usagelimits
Revises: pr048invoice
Create Date: 2026-08-22
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "pr050usagelimits"
down_revision: Union[str, None] = "pr048invoice"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "plans",
        sa.Column(
            "limits",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )

    op.create_table(
        "usage_records",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "organisation_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "subscription_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "resource",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "period_start",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "period_end",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "used",
            sa.Integer(),
            nullable=False,
            server_default="0",
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
        sa.UniqueConstraint(
            "organisation_id",
            "subscription_id",
            "resource",
            "period_start",
            "period_end",
            name="uq_usage_records_period_resource",
        ),
    )

    op.create_index(
        "ix_usage_records_organisation_id",
        "usage_records",
        ["organisation_id"],
    )
    op.create_index(
        "ix_usage_records_subscription_id",
        "usage_records",
        ["subscription_id"],
    )
    op.create_index(
        "ix_usage_records_resource",
        "usage_records",
        ["resource"],
    )
    op.create_index(
        "ix_usage_records_period",
        "usage_records",
        ["period_start", "period_end"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_usage_records_period",
        table_name="usage_records",
    )
    op.drop_index(
        "ix_usage_records_resource",
        table_name="usage_records",
    )
    op.drop_index(
        "ix_usage_records_subscription_id",
        table_name="usage_records",
    )
    op.drop_index(
        "ix_usage_records_organisation_id",
        table_name="usage_records",
    )
    op.drop_table("usage_records")

    op.drop_column("plans", "limits")
