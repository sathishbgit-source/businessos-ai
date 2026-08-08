from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    NotificationAccessDenied,
    NotificationNotFound,
)
from app.db.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class MarkNotificationReadService:
    """Service responsible for marking a notification as read."""

    def __init__(
        self,
        db: AsyncSession,
        notification_repository: NotificationRepository,
    ) -> None:
        self.db = db
        self.notification_repository = notification_repository

    async def execute(
        self,
        *,
        notification_id: UUID,
        user_id: UUID,
    ) -> Notification:
        """Mark a user's notification as read."""

        notification = await self.notification_repository.get_by_id(
            notification_id
        )

        if notification is None:
            raise NotificationNotFound(
                f"Notification with id '{notification_id}' does not exist."
            )

        if notification.user_id != user_id:
            raise NotificationAccessDenied(
                "User is not authorised to access this notification."
            )

        notification = await self.notification_repository.mark_as_read(
            notification
        )

        await self.db.commit()
        await self.db.refresh(notification)

        return notification
