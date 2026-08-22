from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.enums.plan import BillingInterval, PlanStatus


class Plan(Base):
    """Global subscription plan available to organisations."""

    __tablename__ = "plans"

    __table_args__ = (
        Index("ix_plans_code", "code", unique=True),
        Index("ix_plans_status", "status"),
        Index("ix_plans_billing_interval", "billing_interval"),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    billing_interval: Mapped[BillingInterval] = mapped_column(
        String(20),
        nullable=False,
    )

    features: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    limits: Mapped[dict[str, int]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    status: Mapped[PlanStatus] = mapped_column(
        String(20),
        default=PlanStatus.ACTIVE,
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
            f"Plan("
            f"id={self.id}, "
            f"code='{self.code}', "
            f"name='{self.name}', "
            f"status='{self.status}')"
        )
