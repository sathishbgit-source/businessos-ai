from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.notification import Notification


class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        notification: Notification,
    ) -> Notification:
        self.session.add(notification)
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def get_by_id(
        self,
        notification_id: UUID,
    ) -> Notification | None:
        result = await self.session.execute(
            select(Notification).where(
                Notification.id == notification_id
            )
        )
        return result.scalar_one_or_none()

    async def list_for_user(
        self,
        user_id: UUID,
        organisation_id: UUID | None = None,
        unread_only: bool = False,
    ) -> list[Notification]:
        query = select(Notification).where(
            Notification.user_id == user_id
        )

        if organisation_id is not None:
            query = query.where(
                Notification.organisation_id == organisation_id
            )

        if unread_only:
            query = query.where(
                Notification.is_read.is_(False)
            )

        query = query.order_by(
            Notification.created_at.desc()
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def count_unread(
        self,
        user_id: UUID,
        organisation_id: UUID | None = None,
    ) -> int:
        query = select(
            func.count(Notification.id)
        ).where(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )

        if organisation_id is not None:
            query = query.where(
                Notification.organisation_id == organisation_id
            )

        result = await self.session.execute(query)

        return result.scalar_one()

    async def mark_as_read(
        self,
        notification: Notification,
    ) -> Notification:
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.utcnow()

        return notification

    async def mark_all_as_read(
        self,
        user_id: UUID,
        organisation_id: UUID | None = None,
    ) -> int:
        query = select(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )

        if organisation_id is not None:
            query = query.where(
                Notification.organisation_id == organisation_id
            )

        result = await self.session.execute(query)

        notifications = list(result.scalars().all())

        now = datetime.utcnow()

        for notification in notifications:
            notification.is_read = True
            notification.read_at = now

        return len(notifications)
