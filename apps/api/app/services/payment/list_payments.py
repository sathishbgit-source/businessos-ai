from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PaymentAccessDenied
from app.db.enums import MemberStatus, PaymentStatus
from app.db.models.payment import Payment
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.payment_repository import PaymentRepository


class ListPaymentsService:
    """Service responsible for listing organisation payments."""

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
        organisation_id: UUID,
        user_id: UUID,
        status: PaymentStatus | None = None,
    ) -> list[Payment]:
        """Return payments for an organisation, optionally filtered by status."""

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        if status is not None:
            return await self.payment_repository.get_all_by_organisation_and_status(
                organisation_id=organisation_id,
                status=status,
            )

        return await self.payment_repository.get_all_by_organisation(
            organisation_id=organisation_id,
        )

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
