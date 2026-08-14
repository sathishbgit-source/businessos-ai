from datetime import datetime
from decimal import Decimal
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
from app.db.enums.payment import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    __table_args__ = (
        Index(
            "ix_payments_organisation_id",
            "organisation_id",
        ),
        Index(
            "ix_payments_billing_record_id",
            "billing_record_id",
        ),
        Index(
            "ix_payments_subscription_id",
            "subscription_id",
        ),
        Index(
            "ix_payments_customer_id",
            "customer_id",
        ),
        Index(
            "ix_payments_status",
            "status",
        ),
        Index(
            "ix_payments_provider_payment_id",
            "provider_payment_id",
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

    billing_record_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "billing_records.id",
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

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[PaymentStatus] = mapped_column(
        String(20),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    provider_payment_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
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

    def __repr__(self) -> str:
        return (
            f"Payment("
            f"id={self.id}, "
            f"billing_record_id={self.billing_record_id}, "
            f"amount={self.amount}, "
            f"currency='{self.currency}', "
            f"status='{self.status}', "
            f"provider='{self.provider}')"
        )
