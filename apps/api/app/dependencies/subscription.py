from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)
from app.services.subscription.create_subscription import (
    CreateSubscriptionService,
)
from app.services.subscription.get_subscription import (
    GetSubscriptionService,
)
from app.services.subscription.list_subscriptions import (
    ListSubscriptionsService,
)
from app.services.subscription.update_subscription import (
    UpdateSubscriptionService,
)


def get_create_subscription_service(
    db: AsyncSession = Depends(get_db),
) -> CreateSubscriptionService:
    return CreateSubscriptionService(
        db=db,
        subscription_repository=SubscriptionRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_get_subscription_service(
    db: AsyncSession = Depends(get_db),
) -> GetSubscriptionService:
    return GetSubscriptionService(
        db=db,
        subscription_repository=SubscriptionRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_list_subscriptions_service(
    db: AsyncSession = Depends(get_db),
) -> ListSubscriptionsService:
    return ListSubscriptionsService(
        db=db,
        subscription_repository=SubscriptionRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_update_subscription_service(
    db: AsyncSession = Depends(get_db),
) -> UpdateSubscriptionService:
    return UpdateSubscriptionService(
        db=db,
        subscription_repository=SubscriptionRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )
