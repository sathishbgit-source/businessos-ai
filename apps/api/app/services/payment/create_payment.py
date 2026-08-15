from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BillingRecordNotFound,
    OrganisationAccessDenied,
    SubscriptionNotFound,
)
from app.db.enums import MemberStatus, PaymentStatus
from app.db.models.payment import Payment
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import (
    SubscriptionRepository,
)


class CreatePaymentService:
    """Service responsible for creating payments."""

    def __init__(
        self,
        db: AsyncSession,
        payment_repository: PaymentRepository,
        organisation_member_repository: OrganisationMemberRepository,
        billing_repository: BillingRepository,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self.db = db
        self.payment_repository = payment_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )
        self.billing_repository = billing_repository
        self.subscription_repository = subscription_repository

    async def execute(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
        billing_record_id: UUID,
        subscription_id: UUID,
        customer_id: UUID,
        amount: Decimal,
        currency: str,
        provider: str,
        provider_payment_id: str | None = None,
    ) -> Payment:
        """Create a payment after validating organisation access and relationships."""

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        billing_record = await self.billing_repository.get_by_id(
            billing_record_id
        )

        if billing_record is None:
            raise BillingRecordNotFound(
                f"Billing record with id '{billing_record_id}' does not exist."
            )

        if billing_record.organisation_id != organisation_id:
            raise OrganisationAccessDenied(
                "Billing record does not belong to this organisation."
            )

        subscription = await self.subscription_repository.get_by_id(
            subscription_id
        )

        if subscription is None:
            raise SubscriptionNotFound(
                f"Subscription with id '{subscription_id}' does not exist."
            )

        if subscription.organisation_id != organisation_id:
            raise OrganisationAccessDenied(
                "Subscription does not belong to this organisation."
            )

        if subscription.customer_id != customer_id:
            raise ValueError(
                "Payment customer does not match the subscription customer."
            )

        payment = Payment(
            organisation_id=organisation_id,
            billing_record_id=billing_record_id,
            subscription_id=subscription_id,
            customer_id=customer_id,
            amount=amount,
            currency=currency.upper(),
            status=PaymentStatus.PENDING,
            provider=provider,
            provider_payment_id=provider_payment_id,
        )

        payment = await self.payment_repository.create(payment)

        await self.db.commit()
        await self.db.refresh(payment)

        return payment

    async def _validate_access(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
    ) -> None:
        """Ensure the user is an active organisation member."""

        member = (
            await self.organisation_member_repository
            .get_by_organisation_and_user(
                organisation_id=organisation_id,
                user_id=user_id,
            )
        )

        if member is None or member.status != MemberStatus.ACTIVE:
            raise OrganisationAccessDenied(
                "User is not authorised to manage this organisation's payments."
            )
