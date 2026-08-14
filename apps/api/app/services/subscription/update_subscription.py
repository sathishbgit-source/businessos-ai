from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvalidSubscriptionPeriod,
    OrganisationAccessDenied,
    SubscriptionAccessDenied,
    SubscriptionNotFound,
    SubscriptionStateTransitionDenied,
)
from app.db.enums import MemberStatus, SubscriptionStatus
from app.db.models.subscription import Subscription
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)


class UpdateSubscriptionService:
    """Service responsible for updating subscriptions."""

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
        status: SubscriptionStatus | None = None,
        current_period_start: datetime | None = None,
        current_period_end: datetime | None = None,
    ) -> Subscription:
        """Update a subscription after validating access and lifecycle rules."""

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

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        resulting_start = (
            current_period_start
            if current_period_start is not None
            else subscription.current_period_start
        )

        resulting_end = (
            current_period_end
            if current_period_end is not None
            else subscription.current_period_end
        )

        if resulting_end <= resulting_start:
            raise InvalidSubscriptionPeriod(
                "Subscription period end must be after period start."
            )

        if resulting_start < subscription.start_date:
            raise InvalidSubscriptionPeriod(
                "Current period start cannot be before subscription start date."
            )

        if status is not None:
            self._validate_status_transition(
                current_status=subscription.status,
                requested_status=status,
            )

        subscription.current_period_start = resulting_start
        subscription.current_period_end = resulting_end

        if status is not None:
            subscription.status = status

        subscription = await self.subscription_repository.update(
            subscription
        )

        await self.db.commit()
        await self.db.refresh(subscription)

        return subscription

    @staticmethod
    def _validate_status_transition(
        *,
        current_status: SubscriptionStatus,
        requested_status: SubscriptionStatus,
    ) -> None:
        if current_status == requested_status:
            return

        if (
            current_status == SubscriptionStatus.ACTIVE
            and requested_status == SubscriptionStatus.CANCELLED
        ):
            return

        raise SubscriptionStateTransitionDenied(
            f"Subscription cannot transition from "
            f"'{current_status.value}' to '{requested_status.value}'."
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
                "User is not authorised to manage this organisation's subscriptions."
            )
