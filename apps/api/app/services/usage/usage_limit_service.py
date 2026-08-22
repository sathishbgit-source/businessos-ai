from uuid import UUID

from app.core.exceptions import (
    UsageLimitConfigurationError,
    UsageLimitExceeded,
)
from app.db.enums.usage import UsageResource
from app.db.models.usage_record import UsageRecord
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)
from app.repositories.usage_repository import UsageRepository


class UsageLimitService:
    """Resolve and enforce quantitative subscription usage limits."""

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        plan_repository: PlanRepository,
        usage_repository: UsageRepository,
    ) -> None:
        self.subscription_repository = subscription_repository
        self.plan_repository = plan_repository
        self.usage_repository = usage_repository

    async def _get_subscription(
        self,
        *,
        organisation_id: UUID,
    ):
        return await self.subscription_repository.get_active_by_organisation(
            organisation_id=organisation_id,
        )

    async def _get_limit_context(
        self,
        *,
        organisation_id: UUID,
        resource: UsageResource,
    ):
        subscription = await self._get_subscription(
            organisation_id=organisation_id,
        )

        if subscription is None:
            return None, None, None

        plan = await self.plan_repository.get_by_id(
            subscription.plan_id,
        )

        if plan is None:
            raise UsageLimitConfigurationError(
                f"Active subscription '{subscription.id}' references "
                f"missing plan '{subscription.plan_id}'."
            )

        limits = plan.limits or {}

        if resource.value not in limits:
            raise UsageLimitConfigurationError(
                f"Plan '{plan.id}' has no configured limit for "
                f"resource '{resource.value}'."
            )

        limit = limits[resource.value]

        if not isinstance(limit, int) or isinstance(limit, bool):
            raise UsageLimitConfigurationError(
                f"Plan '{plan.id}' has an invalid limit for "
                f"resource '{resource.value}'."
            )

        if limit < 0:
            raise UsageLimitConfigurationError(
                f"Plan '{plan.id}' has a negative limit for "
                f"resource '{resource.value}'."
            )

        return subscription, plan, limit

    async def get_limit(
        self,
        *,
        organisation_id: UUID,
        resource: UsageResource,
    ) -> int | None:
        """Return the configured limit for an organisation's active plan."""

        _, _, limit = await self._get_limit_context(
            organisation_id=organisation_id,
            resource=resource,
        )

        return limit

    async def get_usage(
        self,
        *,
        organisation_id: UUID,
        resource: UsageResource,
    ) -> int:
        """Return usage for the active subscription's current billing period."""

        subscription = await self._get_subscription(
            organisation_id=organisation_id,
        )

        if subscription is None:
            return 0

        record = await self.usage_repository.get(
            organisation_id=organisation_id,
            subscription_id=subscription.id,
            resource=resource,
            period_start=subscription.current_period_start,
            period_end=subscription.current_period_end,
        )

        if record is None:
            return 0

        return record.used

    async def check_limit(
        self,
        *,
        organisation_id: UUID,
        resource: UsageResource,
        quantity: int = 1,
    ) -> bool:
        """Return whether a requested quantity fits within the plan limit."""

        if quantity <= 0:
            raise ValueError("quantity must be greater than zero")

        subscription, _, limit = await self._get_limit_context(
            organisation_id=organisation_id,
            resource=resource,
        )

        if subscription is None:
            return False

        usage = await self.usage_repository.get(
            organisation_id=organisation_id,
            subscription_id=subscription.id,
            resource=resource,
            period_start=subscription.current_period_start,
            period_end=subscription.current_period_end,
        )

        current_usage = usage.used if usage is not None else 0

        return current_usage + quantity <= limit

    async def consume(
        self,
        *,
        organisation_id: UUID,
        resource: UsageResource,
        quantity: int = 1,
    ) -> UsageRecord:
        """Atomically consume usage within the active subscription limit."""

        if quantity <= 0:
            raise ValueError("quantity must be greater than zero")

        subscription, _, limit = await self._get_limit_context(
            organisation_id=organisation_id,
            resource=resource,
        )

        if subscription is None:
            raise UsageLimitExceeded(
                resource=resource.value,
                limit=0,
                current_usage=0,
                requested_quantity=quantity,
            )

        record = await self.usage_repository.get(
            organisation_id=organisation_id,
            subscription_id=subscription.id,
            resource=resource,
            period_start=subscription.current_period_start,
            period_end=subscription.current_period_end,
        )

        current_usage = record.used if record is not None else 0

        consumed = await self.usage_repository.consume_if_within_limit(
            organisation_id=organisation_id,
            subscription_id=subscription.id,
            resource=resource,
            period_start=subscription.current_period_start,
            period_end=subscription.current_period_end,
            limit=limit,
            quantity=quantity,
        )

        if consumed is None:
            raise UsageLimitExceeded(
                resource=resource.value,
                limit=limit,
                current_usage=current_usage,
                requested_quantity=quantity,
            )

        return consumed
