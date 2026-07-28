from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrganisationCreate(BaseModel):
    """Request schema for creating an organisation."""

    name: str = Field(..., min_length=3, max_length=100)
    slug: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class OrganisationUpdate(BaseModel):
    """Request schema for updating an organisation."""

    name: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class OrganisationResponse(BaseModel):
    """Response schema for organisation."""

    id: UUID
    name: str
    slug: str
    description: str | None
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)