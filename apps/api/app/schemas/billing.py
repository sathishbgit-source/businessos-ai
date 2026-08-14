from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.enums import BillingStatus


class BillingRecordCreate(BaseModel):
    """Request schema for creating a billing record."""

    subscription_id: UUID
    billing_period_start: datetime
    billing_period_end: datetime


class BillingRecordUpdate(BaseModel):
    """Request schema for updating a billing record."""

    status: BillingStatus | None = None


class BillingRecordResponse(BaseModel):
    """Response schema for a billing record."""

    id: UUID
    organisation_id: UUID
    subscription_id: UUID
    customer_id: UUID
    plan_id: UUID
    billing_period_start: datetime
    billing_period_end: datetime
    amount: Decimal
    currency: str
    status: BillingStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BillingRecordListResponse(BaseModel):
    """Response schema for billing record listings."""

    items: list[BillingRecordResponse]
    total: int
