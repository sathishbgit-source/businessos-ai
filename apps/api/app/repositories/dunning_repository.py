from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enums.dunning import DunningStatus
from app.db.models.dunning import DunningRecord


class DunningRepository:
    """Persistence operations for dunning records."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_billing_record(
        self,
        *,
        organisation_id: UUID,
        billing_record_id: UUID,
    ) -> DunningRecord | None:
        result = await self.session.execute(
            select(DunningRecord).where(
                DunningRecord.organisation_id == organisation_id,
                DunningRecord.billing_record_id == billing_record_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        *,
        organisation_id: UUID,
        dunning_id: UUID,
    ) -> DunningRecord | None:
        result = await self.session.execute(
            select(DunningRecord).where(
                DunningRecord.organisation_id == organisation_id,
                DunningRecord.id == dunning_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_retryable(
        self,
        *,
        organisation_id: UUID,
        now,
    ) -> list[DunningRecord]:
        result = await self.session.execute(
            select(DunningRecord).where(
                DunningRecord.organisation_id == organisation_id,
                DunningRecord.status == DunningStatus.RETRYING,
                DunningRecord.next_retry_at.is_not(None),
                DunningRecord.next_retry_at <= now,
            )
        )
        return list(result.scalars().all())

    async def add(
        self,
        dunning: DunningRecord,
    ) -> DunningRecord:
        self.session.add(dunning)
        await self.session.flush()
        return dunning
