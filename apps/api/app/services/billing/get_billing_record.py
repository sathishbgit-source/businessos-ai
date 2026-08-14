from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BillingRecordAccessDenied,
    BillingRecordNotFound,
)
from app.db.enums import MemberStatus
from app.db.models.billing_record import BillingRecord
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)


class GetBillingRecordService:
    """Service responsible for retrieving a billing record."""

    def __init__(
        self,
        db: AsyncSession,
        billing_repository: BillingRepository,
        organisation_member_repository: OrganisationMemberRepository,
    ) -> None:
        self.db = db
        self.billing_repository = billing_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )

    async def execute(
        self,
        *,
        billing_record_id: UUID,
        user_id: UUID,
    ) -> BillingRecord:
        """Return a billing record after validating organisation access."""

        billing_record = await self.billing_repository.get_by_id(
            billing_record_id
        )

        if billing_record is None:
            raise BillingRecordNotFound(
                f"Billing record with id '{billing_record_id}' does not exist."
            )

        await self._validate_access(
            organisation_id=billing_record.organisation_id,
            user_id=user_id,
        )

        return billing_record

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
            raise BillingRecordAccessDenied(
                "User is not authorised to access this organisation's billing."
            )
