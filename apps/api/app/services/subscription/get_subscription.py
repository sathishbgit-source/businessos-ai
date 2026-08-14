from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    OrganisationAccessDenied,
    SubscriptionAccessDenied,
    SubscriptionNotFound,
)
from app.db.enums import MemberStatus
from app.db.models.subscription import Subscription
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)


class GetSubscriptionService:
    """Service responsible for retrieving a subscription."""

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
        subscription_id: UUID,
        organisation_id: UUID,
        user_id: UUID,
    ) -> Subscription:
        """Retrieve a subscription after validating access."""

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        subscription = await self.subscription_repository.get_by_id(
            subscription_id
        )

        if subscription is None:
            raise SubscriptionNotFound(
                f"Subscription with id '{subscription_id}' does not exist."
            )

        if subscription.organisation_id != organisation_id:
            raise SubscriptionAccessDenied(
                "Subscription does not belong to this organisation."
            )

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
                "User is not authorised to access this organisation."
            )
