from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from app.db.enums.notification import NotificationType
from app.schemas.pagination import PaginationResponse


class NotificationCreate(BaseModel):
    user_id: UUID
    organisation_id: UUID | None = None
    type: NotificationType
    title: str
    message: str
    data: dict | None = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    organisation_id: UUID | None
    type: NotificationType
    title: str
    message: str
    data: dict | None
    is_read: bool
    read_at: datetime | None
    created_at: datetime


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    pagination: PaginationResponse


class UnreadNotificationCountResponse(BaseModel):
    count: int


class MarkNotificationReadResponse(BaseModel):
    id: UUID
    is_read: bool
    read_at: datetime | None
