from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import OrganisationAccessDenied
from app.db.enums import MemberStatus
from app.db.models.billing_record import BillingRecord
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)


class CreateBillingRecordService:
    """Service responsible for creating billing records."""

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
        organisation_id: UUID,
        user_id: UUID,
        subscription_id: UUID,
        customer_id: UUID,
        plan_id: UUID,
        billing_period_start: datetime,
        billing_period_end: datetime,
        amount: Decimal,
        currency: str,
    ) -> BillingRecord:
        """Create a billing record after validating organisation access."""

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        billing_record = BillingRecord(
            organisation_id=organisation_id,
            subscription_id=subscription_id,
            customer_id=customer_id,
            plan_id=plan_id,
            billing_period_start=billing_period_start,
            billing_period_end=billing_period_end,
            amount=amount,
            currency=currency,
        )

        billing_record = await self.billing_repository.create(
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
            raise OrganisationAccessDenied(
                "User is not authorised to manage this organisation's billing."
            )
