from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.db.enums.billing import BillingStatus


class BillingRecord(Base):
    __tablename__ = "billing_records"

    __table_args__ = (
        Index(
            "ix_billing_records_organisation_id",
            "organisation_id",
        ),
        Index(
            "ix_billing_records_subscription_id",
            "subscription_id",
        ),
        Index(
            "ix_billing_records_customer_id",
            "customer_id",
        ),
        Index(
            "ix_billing_records_plan_id",
            "plan_id",
        ),
        Index(
            "ix_billing_records_status",
            "status",
        ),
        Index(
            "ix_billing_records_billing_period_end",
            "billing_period_end",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    organisation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "organisations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    subscription_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "subscriptions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    plan_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    billing_period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    billing_period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[BillingStatus] = mapped_column(
        String(20),
        default=BillingStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"BillingRecord("
            f"id={self.id}, "
            f"subscription_id={self.subscription_id}, "
            f"amount={self.amount}, "
            f"currency='{self.currency}', "
            f"status='{self.status}')"
        )
