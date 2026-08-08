from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.notification_repository import NotificationRepository


class CountUnreadNotificationsService:
    """Service responsible for counting unread user notifications."""

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
        """Return the number of unread notifications."""

        return await self.notification_repository.count_unread(
            user_id=user_id,
            organisation_id=organisation_id,
        )
