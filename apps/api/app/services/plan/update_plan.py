from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PlanAccessDenied, PlanNotFound
from app.db.enums import BillingInterval, PlanStatus
from app.db.models.plan import Plan
from app.repositories.plan_repository import PlanRepository


class UpdatePlanService:
    """Service responsible for updating subscription plans."""

    def __init__(
        self,
        db: AsyncSession,
        plan_repository: PlanRepository,
    ) -> None:
        self.db = db
        self.plan_repository = plan_repository

    async def execute(
        self,
        *,
        plan_id: UUID,
        is_superuser: bool,
        name: str | None = None,
        description: str | None = None,
        price: Decimal | None = None,
        currency: str | None = None,
        billing_interval: BillingInterval | None = None,
        features: list[str] | None = None,
        status: PlanStatus | None = None,
    ) -> Plan:
        if not is_superuser:
            raise PlanAccessDenied(
                "Only platform administrators can manage plans."
            )

        plan = await self.plan_repository.get_by_id(plan_id)

        if plan is None:
            raise PlanNotFound(
                f"Plan with id '{plan_id}' does not exist."
            )

        if name is not None:
            plan.name = name

        if description is not None:
            plan.description = description

        if price is not None:
            plan.price = price

        if currency is not None:
            plan.currency = currency

        if billing_interval is not None:
            plan.billing_interval = billing_interval

        if features is not None:
            plan.features = features

        if status is not None:
            plan.status = status

        plan = await self.plan_repository.update(plan)

        await self.db.commit()
        await self.db.refresh(plan)

        return plan
