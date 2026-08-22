from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    OrganisationAccessDenied,
    PlanInactive,
    PlanNotFound,
    SubscriptionNotFound,
    SubscriptionStateTransitionDenied,
)
from app.db.enums import MemberStatus, PlanStatus, SubscriptionStatus
from app.db.models.billing_record import BillingRecord
from app.db.models.subscription import Subscription
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)
from app.services.billing.billing_cycle import BillingCycleService


class RenewSubscriptionService:
    """Renew an active subscription into its next billing period."""

    def __init__(
        self,
        db: AsyncSession,
        billing_repository: BillingRepository,
        organisation_member_repository: OrganisationMemberRepository,
        plan_repository: PlanRepository,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self.db = db
        self.billing_repository = billing_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )
        self.plan_repository = plan_repository
        self.subscription_repository = subscription_repository

    async def execute(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
        subscription_id: UUID,
    ) -> Subscription:
        """Renew an active subscription atomically."""

        subscription = await self.subscription_repository.get_by_id(
            subscription_id
        )

        if subscription is None:
            raise SubscriptionNotFound(
                f"Subscription with id '{subscription_id}' does not exist."
            )

        if subscription.organisation_id != organisation_id:
            raise OrganisationAccessDenied(
                "Subscription does not belong to this organisation."
            )

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        if subscription.status != SubscriptionStatus.ACTIVE:
            raise SubscriptionStateTransitionDenied(
                f"Subscription with id '{subscription_id}' "
                f"cannot be renewed from status "
                f"'{subscription.status.value}'."
            )

        plan = await self.plan_repository.get_by_id(
            subscription.plan_id
        )

        if plan is None:
            raise PlanNotFound(
                f"Plan with id '{subscription.plan_id}' does not exist."
            )

        if plan.status != PlanStatus.ACTIVE:
            raise PlanInactive(
                f"Plan '{plan.code}' is not active."
            )

        period = BillingCycleService.calculate_next_period(
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            billing_interval=plan.billing_interval,
        )

        billing_record = BillingRecord(
            organisation_id=organisation_id,
            subscription_id=subscription.id,
            customer_id=subscription.customer_id,
            plan_id=plan.id,
            billing_period_start=period.start,
            billing_period_end=period.end,
            amount=plan.price,
            currency=plan.currency,
        )

        await self.billing_repository.create(billing_record)

        subscription.current_period_start = period.start
        subscription.current_period_end = period.end

        await self.subscription_repository.update(subscription)

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
