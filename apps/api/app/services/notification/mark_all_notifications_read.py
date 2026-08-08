from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class MarkAllNotificationsReadService:
    """Service responsible for marking all user notifications as read."""

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
        user_id: UUID,
        organisation_id: UUID | None = None,
    ) -> int:
        """Mark all unread notifications as read."""

        count = await self.notification_repository.mark_all_as_read(
            user_id=user_id,
            organisation_id=organisation_id,
        )

        await self.db.commit()

        return count
