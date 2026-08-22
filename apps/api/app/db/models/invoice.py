from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.db.enums.invoice import InvoiceStatus


class Invoice(Base):
    __tablename__ = "invoices"

    __table_args__ = (
        Index(
            "ix_invoices_organisation_id",
            "organisation_id",
        ),
        Index(
            "ix_invoices_customer_id",
            "customer_id",
        ),
        Index(
            "ix_invoices_subscription_id",
            "subscription_id",
        ),
        Index(
            "ix_invoices_billing_record_id",
            "billing_record_id",
        ),
        Index(
            "ix_invoices_status",
            "status",
        ),
        Index(
            "ix_invoices_due_at",
            "due_at",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    invoice_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
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
        unique=True,
    )

    billing_period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    billing_period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[InvoiceStatus] = mapped_column(
        String(20),
        default=InvoiceStatus.DRAFT,
        nullable=False,
    )

    payment_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    due_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"Invoice("
            f"id={self.id}, "
            f"invoice_number='{self.invoice_number}', "
            f"total={self.total}, "
            f"currency='{self.currency}', "
            f"status='{self.status}')"
        )
