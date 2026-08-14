from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvalidBillingPeriod,
    OrganisationAccessDenied,
    PlanInactive,
    PlanNotFound,
    SubscriptionNotFound,
)
from app.db.enums import MemberStatus, PlanStatus
from app.db.models.billing_record import BillingRecord
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)


class CreateBillingRecordService:
    """Service responsible for creating billing records."""

    def __init__(
        self,
        db: AsyncSession,
        billing_repository: BillingRepository,
        organisation_member_repository: OrganisationMemberRepository,
        subscription_repository: SubscriptionRepository,
        plan_repository: PlanRepository,
    ) -> None:
        self.db = db
        self.billing_repository = billing_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )
        self.subscription_repository = subscription_repository
        self.plan_repository = plan_repository

    async def execute(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
        subscription_id: UUID,
        billing_period_start: datetime,
        billing_period_end: datetime,
    ) -> BillingRecord:
        """Create a billing record from the authoritative subscription and plan."""

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        if billing_period_end <= billing_period_start:
            raise InvalidBillingPeriod(
                "Billing period end must be after billing period start."
            )

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

        billing_record = BillingRecord(
            organisation_id=organisation_id,
            subscription_id=subscription.id,
            customer_id=subscription.customer_id,
            plan_id=plan.id,
            billing_period_start=billing_period_start,
            billing_period_end=billing_period_end,
            amount=plan.price,
            currency=plan.currency,
        )

        billing_record = await self.billing_repository.create(
            billing_record
        )

        await self.db.commit()
        await self.db.refresh(billing_record)

        return billing_record

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
                "User is not authorised to manage this organisation's billing."
            )
