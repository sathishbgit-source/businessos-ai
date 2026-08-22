from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)
from app.services.entitlement.check_feature_access import (
    FeatureEntitlementService,
)


def get_feature_entitlement_service(
    db: AsyncSession = Depends(get_db),
) -> FeatureEntitlementService:
    return FeatureEntitlementService(
        subscription_repository=SubscriptionRepository(db),
        plan_repository=PlanRepository(db),
    )
