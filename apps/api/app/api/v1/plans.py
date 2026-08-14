from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.plan import (
    get_create_plan_service,
    get_get_plan_service,
    get_list_plans_service,
    get_update_plan_service,
)
from app.schemas.plan import (
    PlanCreate,
    PlanListResponse,
    PlanResponse,
    PlanUpdate,
)
from app.services.plan.create_plan import CreatePlanService
from app.services.plan.get_plan import GetPlanService
from app.services.plan.list_plans import ListPlansService
from app.services.plan.update_plan import UpdatePlanService


router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


@router.post(
    "",
    response_model=PlanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_plan(
    request: PlanCreate,
    current_user: User = Depends(get_current_user),
    service: CreatePlanService = Depends(
        get_create_plan_service,
    ),
):
    """Create a subscription plan."""

    plan = await service.execute(
        is_superuser=current_user.is_superuser,
        code=request.code,
        name=request.name,
        description=request.description,
        price=request.price,
        currency=request.currency,
        billing_interval=request.billing_interval,
        features=request.features,
        status=request.status,
    )

    return PlanResponse.model_validate(plan)


@router.get(
    "",
    response_model=PlanListResponse,
)
async def list_plans(
    service: ListPlansService = Depends(
        get_list_plans_service,
    ),
):
    """List subscription plans."""

    plans = await service.execute()

    return PlanListResponse(
        items=[
            PlanResponse.model_validate(plan)
            for plan in plans
        ],
        total=len(plans),
    )


@router.get(
    "/{plan_id}",
    response_model=PlanResponse,
)
async def get_plan(
    plan_id: UUID,
    service: GetPlanService = Depends(
        get_get_plan_service,
    ),
):
    """Get a subscription plan."""

    plan = await service.execute(
        plan_id=plan_id,
    )

    return PlanResponse.model_validate(plan)


@router.patch(
    "/{plan_id}",
    response_model=PlanResponse,
)
async def update_plan(
    plan_id: UUID,
    request: PlanUpdate,
    current_user: User = Depends(get_current_user),
    service: UpdatePlanService = Depends(
        get_update_plan_service,
    ),
):
    """Update a subscription plan."""

    plan = await service.execute(
        plan_id=plan_id,
        is_superuser=current_user.is_superuser,
        name=request.name,
        description=request.description,
        price=request.price,
        currency=request.currency,
        billing_interval=request.billing_interval,
        features=request.features,
        status=request.status,
    )

    return PlanResponse.model_validate(plan)
