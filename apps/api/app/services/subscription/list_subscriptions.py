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


class ListSubscriptionsService:
    """Service responsible for listing organisation subscriptions."""

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
    ) -> list[Subscription]:
        """Return subscriptions for an organisation."""

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        return await self.subscription_repository.get_all_by_organisation(
            organisation_id=organisation_id,
        )

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
