from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrganisationMemberResponse(BaseModel):
    """Response schema for organisation members."""

    id: UUID
    organisation_id: UUID
    user_id: UUID
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)