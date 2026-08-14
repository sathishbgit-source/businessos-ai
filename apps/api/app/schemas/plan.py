from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.db.enums import BillingInterval, PlanStatus


class PlanCreate(BaseModel):
    """Request schema for creating a subscription plan."""

    code: str = Field(
        ...,
        min_length=2,
        max_length=20,
        pattern=r"^[A-Z0-9_-]+$",
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    description: str = Field(
        ...,
        max_length=500,
    )

    price: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    billing_interval: BillingInterval

    features: list[str] = Field(
        default_factory=list,
    )

    status: PlanStatus = PlanStatus.ACTIVE


class PlanUpdate(BaseModel):
    """Request schema for updating a subscription plan."""

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    price: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    billing_interval: BillingInterval | None = None

    features: list[str] | None = None

    status: PlanStatus | None = None


class PlanResponse(BaseModel):
    """Response schema for a subscription plan."""

    id: UUID
    code: str
    name: str
    description: str
    price: Decimal
    currency: str
    billing_interval: BillingInterval
    features: list[str]
    status: PlanStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlanListResponse(BaseModel):
    """Response schema for plan listings."""

    items: list[PlanResponse]
    total: int
