from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PlanAccessDenied, PlanAlreadyExists
from app.db.enums import BillingInterval, PlanStatus
from app.db.models.plan import Plan
from app.repositories.plan_repository import PlanRepository


class CreatePlanService:
    """Service responsible for creating subscription plans."""

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
        is_superuser: bool,
        code: str,
        name: str,
        description: str,
        price: Decimal,
        currency: str,
        billing_interval: BillingInterval,
        features: list[str],
        status: PlanStatus = PlanStatus.ACTIVE,
    ) -> Plan:
        if not is_superuser:
            raise PlanAccessDenied(
                "Only platform administrators can manage plans."
            )

        existing = await self.plan_repository.get_by_code(code)

        if existing:
            raise PlanAlreadyExists(
                f"Plan with code '{code}' already exists."
            )

        plan = Plan(
            code=code,
            name=name,
            description=description,
            price=price,
            currency=currency,
            billing_interval=billing_interval,
            features=features,
            status=status,
        )

        plan = await self.plan_repository.create(plan)

        await self.db.commit()
        await self.db.refresh(plan)

        return plan
