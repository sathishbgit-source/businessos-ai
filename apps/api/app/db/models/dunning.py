from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.db.enums.dunning import DunningStatus


class DunningRecord(Base):
    """Persistent failed-payment recovery state."""

    __tablename__ = "dunning_records"

    __table_args__ = (
        Index(
            "ix_dunning_records_organisation_id",
            "organisation_id",
        ),
        Index(
            "ix_dunning_records_subscription_id",
            "subscription_id",
        ),
        Index(
            "ix_dunning_records_billing_record_id",
            "billing_record_id",
        ),
        Index(
            "ix_dunning_records_status",
            "status",
        ),
        Index(
            "ix_dunning_records_next_retry_at",
            "next_retry_at",
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

    billing_record_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "billing_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    status: Mapped[DunningStatus] = mapped_column(
        String(20),
        nullable=False,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    next_retry_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    grace_period_ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
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
