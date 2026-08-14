from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.plan import Plan


class PlanRepository:
    """Repository responsible for Plan persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        plan_id: UUID,
    ) -> Plan | None:
        result = await self.db.execute(
            select(Plan).where(
                Plan.id == plan_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_code(
        self,
        code: str,
    ) -> Plan | None:
        result = await self.db.execute(
            select(Plan).where(
                Plan.code == code
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Plan]:
        result = await self.db.execute(
            select(Plan).order_by(
                Plan.created_at.desc()
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        plan: Plan,
    ) -> Plan:
        """
        Persist a new plan.

        Transaction commit is handled by the service layer.
        """
        self.db.add(plan)
        await self.db.flush()
        await self.db.refresh(plan)

        return plan

    async def update(
        self,
        plan: Plan,
    ) -> Plan:
        """
        Flush pending plan changes.

        Commit is handled by the service layer.
        """
        await self.db.flush()
        await self.db.refresh(plan)

        return plan
