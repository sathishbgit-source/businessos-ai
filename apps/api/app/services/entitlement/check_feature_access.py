from uuid import UUID

from app.core.exceptions import FeatureNotEntitled
from app.db.enums.entitlement import Feature
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)


class FeatureEntitlementService:
    """Resolve feature entitlements from an organisation's subscription."""

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        plan_repository: PlanRepository,
    ) -> None:
        self.subscription_repository = subscription_repository
        self.plan_repository = plan_repository

    async def has_feature(
        self,
        *,
        organisation_id: UUID,
        feature: Feature,
    ) -> bool:
        """Return whether the organisation is entitled to a feature."""

        subscription = (
            await self.subscription_repository
            .get_active_by_organisation(
                organisation_id=organisation_id,
            )
        )

        if subscription is None:
            return False

        plan = await self.plan_repository.get_by_id(
            subscription.plan_id,
        )

        if plan is None:
            return False

        return feature.value in (plan.features or [])

    async def require_feature(
        self,
        *,
        organisation_id: UUID,
        feature: Feature,
    ) -> None:
        """Require the organisation to be entitled to a feature."""

        if not await self.has_feature(
            organisation_id=organisation_id,
            feature=feature,
        ):
            raise FeatureNotEntitled(
                f"Organisation '{organisation_id}' is not entitled "
                f"to feature '{feature.value}'."
            )
