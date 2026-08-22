from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.enums.usage import UsageResource


class UsageRecord(Base):
    """Persisted usage counter for a subscription billing period."""

    __tablename__ = "usage_records"

    __table_args__ = (
        Index(
            "ix_usage_records_organisation_id",
            "organisation_id",
        ),
        Index(
            "ix_usage_records_subscription_id",
            "subscription_id",
        ),
        Index(
            "ix_usage_records_resource",
            "resource",
        ),
        Index(
            "ix_usage_records_period",
            "period_start",
            "period_end",
        ),
        Index(
            "uq_usage_records_period_resource",
            "organisation_id",
            "subscription_id",
            "resource",
            "period_start",
            "period_end",
            unique=True,
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

    resource: Mapped[UsageResource] = mapped_column(
        String(50),
        nullable=False,
    )

    period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    used: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
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
            f"UsageRecord("
            f"id={self.id}, "
            f"organisation_id={self.organisation_id}, "
            f"subscription_id={self.subscription_id}, "
            f"resource='{self.resource}', "
            f"used={self.used})"
        )
