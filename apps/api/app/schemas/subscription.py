from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.enums import SubscriptionStatus


class SubscriptionCreate(BaseModel):
    """Request schema for creating a subscription."""

    customer_id: UUID
    plan_id: UUID
    start_date: datetime
    current_period_start: datetime
    current_period_end: datetime


class SubscriptionUpdate(BaseModel):
    """Request schema for updating a subscription."""

    status: SubscriptionStatus | None = None
    current_period_start: datetime | None = None
    current_period_end: datetime | None = None


class SubscriptionResponse(BaseModel):
    """Response schema for a subscription."""

    id: UUID
    organisation_id: UUID
    customer_id: UUID
    plan_id: UUID
    status: SubscriptionStatus
    start_date: datetime
    current_period_start: datetime
    current_period_end: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubscriptionListResponse(BaseModel):
    """Response schema for subscription listings."""

    items: list[SubscriptionResponse]
    total: int
