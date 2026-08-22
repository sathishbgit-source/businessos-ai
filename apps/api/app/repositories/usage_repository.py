from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enums.usage import UsageResource
from app.db.models.usage_record import UsageRecord


class UsageRepository:
    """Repository responsible for persisted subscription usage."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(
        self,
        *,
        organisation_id: UUID,
        subscription_id: UUID,
        resource: UsageResource,
        period_start: datetime,
        period_end: datetime,
    ) -> UsageRecord | None:
        result = await self.db.execute(
            select(UsageRecord).where(
                UsageRecord.organisation_id == organisation_id,
                UsageRecord.subscription_id == subscription_id,
                UsageRecord.resource == resource.value,
                UsageRecord.period_start == period_start,
                UsageRecord.period_end == period_end,
            )
        )
        return result.scalar_one_or_none()

    async def get_or_create(
        self,
        *,
        organisation_id: UUID,
        subscription_id: UUID,
        resource: UsageResource,
        period_start: datetime,
        period_end: datetime,
    ) -> UsageRecord:
        now = datetime.now(timezone.utc)

        statement = (
            insert(UsageRecord)
            .values(
                organisation_id=organisation_id,
                subscription_id=subscription_id,
                resource=resource.value,
                period_start=period_start,
                period_end=period_end,
                used=0,
                created_at=now,
                updated_at=now,
            )
            .on_conflict_do_nothing(
                constraint="uq_usage_records_period_resource",
            )
        )

        await self.db.execute(statement)
        await self.db.flush()

        record = await self.get(
            organisation_id=organisation_id,
            subscription_id=subscription_id,
            resource=resource,
            period_start=period_start,
            period_end=period_end,
        )

        if record is None:
            raise RuntimeError(
                "Usage record could not be created or retrieved"
            )

        return record

    async def consume_if_within_limit(
        self,
        *,
        organisation_id: UUID,
        subscription_id: UUID,
        resource: UsageResource,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        quantity: int = 1,
    ) -> UsageRecord | None:
        """
        Atomically consume usage only when the configured limit is not exceeded.

        Returns the updated UsageRecord when consumption succeeds.
        Returns None when the requested quantity would exceed the limit.
        """

        if quantity <= 0:
            raise ValueError("quantity must be greater than zero")

        record = await self.get_or_create(
            organisation_id=organisation_id,
            subscription_id=subscription_id,
            resource=resource,
            period_start=period_start,
            period_end=period_end,
        )

        statement = (
            update(UsageRecord)
            .where(
                UsageRecord.id == record.id,
                UsageRecord.used + quantity <= limit,
            )
            .values(
                used=UsageRecord.used + quantity,
                updated_at=datetime.now(timezone.utc),
            )
            .returning(UsageRecord.id)
        )

        result = await self.db.execute(statement)
        updated_id = result.scalar_one_or_none()

        if updated_id is None:
            return None

        await self.db.flush()

        return await self.db.get(
            UsageRecord,
            updated_id,
        )
