from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    PaymentAccessDenied,
    PaymentNotFound,
)
from app.db.enums import MemberStatus, PaymentStatus
from app.db.models.payment import Payment
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.payment_repository import PaymentRepository


class UpdatePaymentService:
    """Service responsible for updating payments."""

    def __init__(
        self,
        db: AsyncSession,
        payment_repository: PaymentRepository,
        organisation_member_repository: OrganisationMemberRepository,
    ) -> None:
        self.db = db
        self.payment_repository = payment_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )

    async def execute(
        self,
        *,
        payment_id: UUID,
        organisation_id: UUID,
        user_id: UUID,
        status: PaymentStatus | None = None,
        provider_payment_id: str | None = None,
        failure_reason: str | None = None,
        paid_at: datetime | None = None,
    ) -> Payment:
        """Update a payment after validating organisation access."""

        payment = await self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise PaymentNotFound(
                f"Payment with id '{payment_id}' does not exist."
            )

        if payment.organisation_id != organisation_id:
            raise PaymentAccessDenied(
                "Payment does not belong to this organisation."
            )

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        if status is not None:
            payment.status = status

        if provider_payment_id is not None:
            payment.provider_payment_id = provider_payment_id

        if failure_reason is not None:
            payment.failure_reason = failure_reason

        if paid_at is not None:
            payment.paid_at = paid_at

        if status == PaymentStatus.SUCCEEDED and payment.paid_at is None:
            payment.paid_at = datetime.now(timezone.utc)

        payment = await self.payment_repository.update(payment)

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
            raise PaymentAccessDenied(
                "User is not authorised to manage this organisation's payments."
            )
