from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enums.subscription import SubscriptionStatus
from app.db.models.subscription import Subscription


class SubscriptionRepository:
    """Repository responsible for Subscription persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        subscription_id: UUID,
    ) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription).where(
                Subscription.id == subscription_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_organisation(
        self,
        organisation_id: UUID,
    ) -> list[Subscription]:
        result = await self.db.execute(
            select(Subscription)
            .where(
                Subscription.organisation_id == organisation_id
            )
            .order_by(Subscription.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_active_by_organisation(
        self,
        organisation_id: UUID,
    ) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription)
            .where(
                Subscription.organisation_id == organisation_id,
                Subscription.status == SubscriptionStatus.ACTIVE,
            )
            .order_by(Subscription.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_all_by_customer(
        self,
        customer_id: UUID,
    ) -> list[Subscription]:
        result = await self.db.execute(
            select(Subscription)
            .where(
                Subscription.customer_id == customer_id
            )
            .order_by(Subscription.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Persist a new subscription.

        Transaction commit is handled by the service layer.
        """
        self.db.add(subscription)
        await self.db.flush()
        await self.db.refresh(subscription)

        return subscription

    async def update(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Flush pending subscription changes.

        Commit is handled by the service layer.
        """
        await self.db.flush()
        await self.db.refresh(subscription)

        return subscription
