from app.db.models.plan import Plan
from app.repositories.plan_repository import PlanRepository


class ListPlansService:
    """Service responsible for listing subscription plans."""

    def __init__(
        self,
        plan_repository: PlanRepository,
    ) -> None:
        self.plan_repository = plan_repository

    async def execute(self) -> list[Plan]:
        return await self.plan_repository.get_all()
