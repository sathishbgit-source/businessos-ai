from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.plan_repository import PlanRepository
from app.services.plan.create_plan import CreatePlanService
from app.services.plan.get_plan import GetPlanService
from app.services.plan.list_plans import ListPlansService
from app.services.plan.update_plan import UpdatePlanService


def get_create_plan_service(
    db: AsyncSession = Depends(get_db),
) -> CreatePlanService:
    return CreatePlanService(
        db=db,
        plan_repository=PlanRepository(db),
    )


def get_get_plan_service(
    db: AsyncSession = Depends(get_db),
) -> GetPlanService:
    return GetPlanService(
        plan_repository=PlanRepository(db),
    )


def get_list_plans_service(
    db: AsyncSession = Depends(get_db),
) -> ListPlansService:
    return ListPlansService(
        plan_repository=PlanRepository(db),
    )


def get_update_plan_service(
    db: AsyncSession = Depends(get_db),
) -> UpdatePlanService:
    return UpdatePlanService(
        db=db,
        plan_repository=PlanRepository(db),
    )
