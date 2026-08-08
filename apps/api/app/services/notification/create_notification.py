from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFound
from app.db.enums.notification import NotificationType
from app.db.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository


class CreateNotificationService:
    """Service responsible for creating user notifications."""

    def __init__(
        self,
        db: AsyncSession,
        notification_repository: NotificationRepository,
        user_repository: UserRepository,
    ) -> None:
        self.db = db
        self.notification_repository = notification_repository
        self.user_repository = user_repository

    async def execute(
        self,
        *,
        user_id: UUID,
        notification_type: NotificationType,
        title: str,
        message: str,
        organisation_id: UUID | None = None,
        data: dict | None = None,
    ) -> Notification:
        """Create and persist a notification."""

        user = await self.user_repository.get_by_id(
            user_id
        )

        if user is None:
            raise UserNotFound(
                f"User with id '{user_id}' does not exist."
            )

        notification = Notification(
            user_id=user.id,
            organisation_id=organisation_id,
            type=notification_type,
            title=title,
            message=message,
            data=data,
        )

        notification = await self.notification_repository.create(
            notification
        )

        await self.db.commit()
        await self.db.refresh(notification)

        return notification
