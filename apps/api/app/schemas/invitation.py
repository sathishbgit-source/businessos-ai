from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InvitationCreate(BaseModel):
    """Request schema for inviting a user."""

    email: EmailStr
    role: str = Field(..., min_length=2, max_length=50)


class InvitationAccept(BaseModel):
    """Request schema for accepting an invitation."""

    token: str = Field(..., min_length=1)


class InvitationResponse(BaseModel):
    """Response schema for invitation."""

    id: UUID
    organisation_id: UUID
    email: EmailStr
    role: str
    status: str
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)