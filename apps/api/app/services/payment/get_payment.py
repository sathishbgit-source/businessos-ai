from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    PaymentAccessDenied,
    PaymentNotFound,
)
from app.db.enums import MemberStatus
from app.db.models.payment import Payment
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.payment_repository import PaymentRepository


class GetPaymentService:
    """Service responsible for retrieving a payment."""

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
    ) -> Payment:
        """Return a payment after validating organisation access."""

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
                "User is not authorised to access this organisation's payments."
            )
