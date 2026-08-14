from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.services.billing.create_billing_record import (
    CreateBillingRecordService,
)
from app.services.billing.get_billing_record import (
    GetBillingRecordService,
)
from app.services.billing.list_billing_records import (
    ListBillingRecordsService,
)
from app.services.billing.update_billing_record import (
    UpdateBillingRecordService,
)


def get_create_billing_record_service(
    db: AsyncSession = Depends(get_db),
) -> CreateBillingRecordService:
    return CreateBillingRecordService(
        db=db,
        billing_repository=BillingRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_get_billing_record_service(
    db: AsyncSession = Depends(get_db),
) -> GetBillingRecordService:
    return GetBillingRecordService(
        db=db,
        billing_repository=BillingRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_list_billing_records_service(
    db: AsyncSession = Depends(get_db),
) -> ListBillingRecordsService:
    return ListBillingRecordsService(
        db=db,
        billing_repository=BillingRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_update_billing_record_service(
    db: AsyncSession = Depends(get_db),
) -> UpdateBillingRecordService:
    return UpdateBillingRecordService(
        db=db,
        billing_repository=BillingRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )
