from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.billing_record import BillingRecord


class BillingRepository:
    """Repository responsible for BillingRecord persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        billing_record_id: UUID,
    ) -> BillingRecord | None:
        result = await self.db.execute(
            select(BillingRecord).where(
                BillingRecord.id == billing_record_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_organisation(
        self,
        organisation_id: UUID,
    ) -> list[BillingRecord]:
        result = await self.db.execute(
            select(BillingRecord)
            .where(
                BillingRecord.organisation_id == organisation_id
            )
            .order_by(BillingRecord.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_by_subscription(
        self,
        subscription_id: UUID,
    ) -> list[BillingRecord]:
        result = await self.db.execute(
            select(BillingRecord)
            .where(
                BillingRecord.subscription_id == subscription_id
            )
            .order_by(BillingRecord.billing_period_end.desc())
        )
        return list(result.scalars().all())

    async def get_all_by_customer(
        self,
        customer_id: UUID,
    ) -> list[BillingRecord]:
        result = await self.db.execute(
            select(BillingRecord)
            .where(
                BillingRecord.customer_id == customer_id
            )
            .order_by(BillingRecord.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        billing_record: BillingRecord,
    ) -> BillingRecord:
        """
        Persist a new billing record.

        Transaction commit is handled by the service layer.
        """
        self.db.add(billing_record)
        await self.db.flush()
        await self.db.refresh(billing_record)

        return billing_record

    async def update(
        self,
        billing_record: BillingRecord,
    ) -> BillingRecord:
        """
        Flush pending billing record changes.

        Commit is handled by the service layer.
        """
        await self.db.flush()
        await self.db.refresh(billing_record)

        return billing_record
