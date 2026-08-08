from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class ListNotificationsService:
    """Service responsible for listing user notifications."""

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
        unread_only: bool = False,
    ) -> list[Notification]:
        """Return notifications belonging to the authenticated user."""

        return await self.notification_repository.list_for_user(
            user_id=user_id,
            organisation_id=organisation_id,
            unread_only=unread_only,
        )
