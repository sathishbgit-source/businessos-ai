from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.services.notification.count_unread_notifications import (
    CountUnreadNotificationsService,
)
from app.services.notification.list_notifications import (
    ListNotificationsService,
)
from app.services.notification.mark_all_notifications_read import (
    MarkAllNotificationsReadService,
)
from app.services.notification.mark_notification_read import (
    MarkNotificationReadService,
)


def get_list_notifications_service(
    db: AsyncSession = Depends(get_db),
) -> ListNotificationsService:
    """Create ListNotificationsService."""

    return ListNotificationsService(
        db=db,
        notification_repository=NotificationRepository(db),
    )


def get_count_unread_notifications_service(
    db: AsyncSession = Depends(get_db),
) -> CountUnreadNotificationsService:
    """Create CountUnreadNotificationsService."""

    return CountUnreadNotificationsService(
        db=db,
        notification_repository=NotificationRepository(db),
    )


def get_mark_notification_read_service(
    db: AsyncSession = Depends(get_db),
) -> MarkNotificationReadService:
    """Create MarkNotificationReadService."""

    return MarkNotificationReadService(
        db=db,
        notification_repository=NotificationRepository(db),
    )


def get_mark_all_notifications_read_service(
    db: AsyncSession = Depends(get_db),
) -> MarkAllNotificationsReadService:
    """Create MarkAllNotificationsReadService."""

    return MarkAllNotificationsReadService(
        db=db,
        notification_repository=NotificationRepository(db),
    )
