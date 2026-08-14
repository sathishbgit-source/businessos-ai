from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.db.enums.subscription import SubscriptionStatus


class Subscription(Base):
    __tablename__ = "subscriptions"

    __table_args__ = (
        Index(
            "ix_subscriptions_organisation_id",
            "organisation_id",
        ),
        Index(
            "ix_subscriptions_customer_id",
            "customer_id",
        ),
        Index(
            "ix_subscriptions_plan_id",
            "plan_id",
        ),
        Index(
            "ix_subscriptions_status",
            "status",
        ),
        Index(
            "ix_subscriptions_current_period_end",
            "current_period_end",
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

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    plan_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "plans.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    status: Mapped[SubscriptionStatus] = mapped_column(
        String(20),
        default=SubscriptionStatus.ACTIVE,
        nullable=False,
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    current_period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    current_period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
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
            f"Subscription("
            f"id={self.id}, "
            f"organisation_id={self.organisation_id}, "
            f"customer_id={self.customer_id}, "
            f"plan_id={self.plan_id}, "
            f"status='{self.status}')"
        )
