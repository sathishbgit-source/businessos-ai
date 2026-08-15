from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.enums import PaymentStatus


class PaymentCreate(BaseModel):
    """Request schema for creating a payment."""

    billing_record_id: UUID
    subscription_id: UUID
    customer_id: UUID
    amount: Decimal
    currency: str
    provider: str
    provider_payment_id: str | None = None


class PaymentUpdate(BaseModel):
    """Request schema for updating a payment."""

    status: PaymentStatus | None = None
    provider_payment_id: str | None = None
    failure_reason: str | None = None
    paid_at: datetime | None = None


class PaymentResponse(BaseModel):
    """Response schema for a payment."""

    id: UUID
    organisation_id: UUID
    billing_record_id: UUID
    subscription_id: UUID
    customer_id: UUID
    amount: Decimal
    currency: str
    status: PaymentStatus
    provider: str
    provider_payment_id: str | None
    failure_reason: str | None
    paid_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentListResponse(BaseModel):
    """Response schema for payment listings."""

    items: list[PaymentResponse]
    total: int
