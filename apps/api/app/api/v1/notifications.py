from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.notification import (
    get_count_unread_notifications_service,
    get_list_notifications_service,
    get_mark_all_notifications_read_service,
    get_mark_notification_read_service,
)
from app.schemas.notification import (
    MarkNotificationReadResponse,
    NotificationListResponse,
    NotificationResponse,
    UnreadNotificationCountResponse,
)
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

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "",
    response_model=NotificationListResponse,
)
async def list_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    service: ListNotificationsService = Depends(
        get_list_notifications_service,
    ),
):
    """List notifications for the authenticated user."""

    notifications = await service.execute(
        user_id=current_user.id,
        unread_only=unread_only,
    )

    return NotificationListResponse(
        items=[
            NotificationResponse.model_validate(notification)
            for notification in notifications
        ],
        total=len(notifications),
    )


@router.get(
    "/unread-count",
    response_model=UnreadNotificationCountResponse,
)
async def unread_notification_count(
    current_user: User = Depends(get_current_user),
    service: CountUnreadNotificationsService = Depends(
        get_count_unread_notifications_service,
    ),
):
    """Return the unread notification count."""

    count = await service.execute(
        user_id=current_user.id,
    )

    return UnreadNotificationCountResponse(
        count=count,
    )


@router.patch(
    "/read-all",
)
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    service: MarkAllNotificationsReadService = Depends(
        get_mark_all_notifications_read_service,
    ),
):
    """Mark all notifications for the authenticated user as read."""

    count = await service.execute(
        user_id=current_user.id,
    )

    return {
        "marked_count": count,
    }


@router.patch(
    "/{notification_id}/read",
    response_model=MarkNotificationReadResponse,
)
async def mark_notification_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    service: MarkNotificationReadService = Depends(
        get_mark_notification_read_service,
    ),
):
    """Mark a notification as read."""

    notification = await service.execute(
        notification_id=notification_id,
        user_id=current_user.id,
    )

    return MarkNotificationReadResponse(
        id=notification.id,
        is_read=notification.is_read,
        read_at=notification.read_at,
    )
