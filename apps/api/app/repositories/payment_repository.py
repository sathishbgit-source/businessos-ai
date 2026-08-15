from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enums.payment import PaymentStatus
from app.db.models.payment import Payment


class PaymentRepository:
    """Repository responsible for Payment persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        payment_id: UUID,
    ) -> Payment | None:
        result = await self.db.execute(
            select(Payment).where(
                Payment.id == payment_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_organisation(
        self,
        organisation_id: UUID,
    ) -> list[Payment]:
        result = await self.db.execute(
            select(Payment)
            .where(
                Payment.organisation_id == organisation_id
            )
            .order_by(Payment.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_by_billing_record(
        self,
        billing_record_id: UUID,
    ) -> list[Payment]:
        result = await self.db.execute(
            select(Payment)
            .where(
                Payment.billing_record_id == billing_record_id
            )
            .order_by(Payment.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_by_subscription(
        self,
        subscription_id: UUID,
    ) -> list[Payment]:
        result = await self.db.execute(
            select(Payment)
            .where(
                Payment.subscription_id == subscription_id
            )
            .order_by(Payment.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_by_customer(
        self,
        customer_id: UUID,
    ) -> list[Payment]:
        result = await self.db.execute(
            select(Payment)
            .where(
                Payment.customer_id == customer_id
            )
            .order_by(Payment.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_provider_payment_id(
        self,
        provider_payment_id: str,
    ) -> Payment | None:
        result = await self.db.execute(
            select(Payment).where(
                Payment.provider_payment_id == provider_payment_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_organisation_and_status(
        self,
        organisation_id: UUID,
        status: PaymentStatus,
    ) -> list[Payment]:
        result = await self.db.execute(
            select(Payment)
            .where(
                Payment.organisation_id == organisation_id,
                Payment.status == status,
            )
            .order_by(Payment.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        payment: Payment,
    ) -> Payment:
        """
        Persist a new payment.

        Transaction commit is handled by the service layer.
        """
        self.db.add(payment)
        await self.db.flush()
        await self.db.refresh(payment)

        return payment

    async def update(
        self,
        payment: Payment,
    ) -> Payment:
        """
        Flush pending payment changes.

        Commit is handled by the service layer.
        """
        await self.db.flush()
        await self.db.refresh(payment)

        return payment
