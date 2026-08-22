from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    OrganisationAccessDenied,
    PlanInactive,
    PlanNotFound,
    SubscriptionNotFound,
)
from app.db.enums import PlanStatus
from app.db.models.billing_record import BillingRecord
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)
from app.services.billing.billing_cycle import BillingCycleService
from app.services.billing.create_billing_record import (
    CreateBillingRecordService,
)


class GenerateBillingPeriodService:
    """Generate and persist the next billing period."""

    def __init__(
        self,
        db: AsyncSession,
        billing_repository: BillingRepository,
        organisation_member_repository: OrganisationMemberRepository,
        subscription_repository: SubscriptionRepository,
        plan_repository: PlanRepository,
    ) -> None:
        self.subscription_repository = subscription_repository
        self.plan_repository = plan_repository

        self.create_billing_record_service = (
            CreateBillingRecordService(
                db=db,
                billing_repository=billing_repository,
                organisation_member_repository=(
                    organisation_member_repository
                ),
                subscription_repository=subscription_repository,
                plan_repository=plan_repository,
            )
        )

    async def execute(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
        subscription_id: UUID,
    ) -> BillingRecord:
        """Generate the next billing period."""

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

        period = BillingCycleService.calculate_next_period(
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            billing_interval=plan.billing_interval,
        )

        return await self.create_billing_record_service.execute(
            organisation_id=organisation_id,
            user_id=user_id,
            subscription_id=subscription_id,
            billing_period_start=period.start,
            billing_period_end=period.end,
        )
