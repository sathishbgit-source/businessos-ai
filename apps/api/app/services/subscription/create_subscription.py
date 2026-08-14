from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import OrganisationAccessDenied
from app.db.enums import MemberStatus
from app.db.models.subscription import Subscription
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)


class CreateSubscriptionService:
    """Service responsible for creating subscriptions."""

    def __init__(
        self,
        db: AsyncSession,
        subscription_repository: SubscriptionRepository,
        organisation_member_repository: OrganisationMemberRepository,
    ) -> None:
        self.db = db
        self.subscription_repository = subscription_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )

    async def execute(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
        customer_id: UUID,
        plan_id: UUID,
        start_date: datetime,
        current_period_start: datetime,
        current_period_end: datetime,
    ) -> Subscription:
        """Create a subscription after validating organisation access."""

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        subscription = Subscription(
            organisation_id=organisation_id,
            customer_id=customer_id,
            plan_id=plan_id,
            start_date=start_date,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
        )

        subscription = await self.subscription_repository.create(
            subscription
        )

        await self.db.commit()
        await self.db.refresh(subscription)

        return subscription

    async def _validate_access(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
    ) -> None:
        """Ensure the user is an active organisation member."""

        member = (
            await self.organisation_member_repository
            .get_by_organisation_and_user(
                organisation_id=organisation_id,
                user_id=user_id,
            )
        )

        if member is None or member.status != MemberStatus.ACTIVE:
            raise OrganisationAccessDenied(
                "User is not authorised to manage this organisation's subscriptions."
            )
