from uuid import UUID

from app.core.exceptions import PlanNotFound
from app.db.models.plan import Plan
from app.repositories.plan_repository import PlanRepository


class GetPlanService:
    """Service responsible for retrieving a subscription plan."""

    def __init__(
        self,
        plan_repository: PlanRepository,
    ) -> None:
        self.plan_repository = plan_repository

    async def execute(
        self,
        *,
        plan_id: UUID,
    ) -> Plan:
        plan = await self.plan_repository.get_by_id(plan_id)

        if plan is None:
            raise PlanNotFound(
                f"Plan with id '{plan_id}' does not exist."
            )

        return plan
