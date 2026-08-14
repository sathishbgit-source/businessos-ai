from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.subscription import (
    get_create_subscription_service,
    get_get_subscription_service,
    get_list_subscriptions_service,
    get_update_subscription_service,
)
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionListResponse,
    SubscriptionResponse,
    SubscriptionUpdate,
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

router = APIRouter(
    prefix="/organisations/{organisation_id}/subscriptions",
    tags=["Subscriptions"],
)


@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    organisation_id: UUID,
    request: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    service: CreateSubscriptionService = Depends(
        get_create_subscription_service,
    ),
):
    """Create a subscription for an organisation."""

    subscription = await service.execute(
        organisation_id=organisation_id,
        user_id=current_user.id,
        customer_id=request.customer_id,
        plan_id=request.plan_id,
        start_date=request.start_date,
        current_period_start=request.current_period_start,
        current_period_end=request.current_period_end,
    )

    return SubscriptionResponse.model_validate(subscription)


@router.get(
    "",
    response_model=SubscriptionListResponse,
)
async def list_subscriptions(
    organisation_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ListSubscriptionsService = Depends(
        get_list_subscriptions_service,
    ),
):
    """List subscriptions for an organisation."""

    subscriptions = await service.execute(
        organisation_id=organisation_id,
        user_id=current_user.id,
    )

    return SubscriptionListResponse(
        items=[
            SubscriptionResponse.model_validate(subscription)
            for subscription in subscriptions
        ],
        total=len(subscriptions),
    )


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
)
async def get_subscription(
    organisation_id: UUID,
    subscription_id: UUID,
    current_user: User = Depends(get_current_user),
    service: GetSubscriptionService = Depends(
        get_get_subscription_service,
    ),
):
    """Get a subscription."""

    subscription = await service.execute(
        subscription_id=subscription_id,
        organisation_id=organisation_id,
        user_id=current_user.id,
    )

    return SubscriptionResponse.model_validate(subscription)


@router.patch(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
)
async def update_subscription(
    organisation_id: UUID,
    subscription_id: UUID,
    request: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    service: UpdateSubscriptionService = Depends(
        get_update_subscription_service,
    ),
):
    """Update a subscription."""

    subscription = await service.execute(
        subscription_id=subscription_id,
        organisation_id=organisation_id,
        user_id=current_user.id,
        status=request.status,
        current_period_start=request.current_period_start,
        current_period_end=request.current_period_end,
    )

    return SubscriptionResponse.model_validate(subscription)
