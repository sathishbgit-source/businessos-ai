from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BillingRecordAccessDenied,
    BillingRecordNotFound,
)
from app.db.enums import BillingStatus, MemberStatus
from app.db.models.billing_record import BillingRecord
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)


class UpdateBillingRecordService:
    """Service responsible for updating billing records."""

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
        organisation_id: UUID,
        user_id: UUID,
        status: BillingStatus | None = None,
    ) -> BillingRecord:
        """Update a billing record after validating organisation access."""

        billing_record = await self.billing_repository.get_by_id(
            billing_record_id
        )

        if billing_record is None:
            raise BillingRecordNotFound(
                f"Billing record with id '{billing_record_id}' does not exist."
            )

        if billing_record.organisation_id != organisation_id:
            raise BillingRecordAccessDenied(
                "Billing record does not belong to this organisation."
            )

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        if status is not None:
            billing_record.status = status

        billing_record = await self.billing_repository.update(
            billing_record
        )

        await self.db.commit()
        await self.db.refresh(billing_record)

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
                "User is not authorised to manage this organisation's billing."
            )
