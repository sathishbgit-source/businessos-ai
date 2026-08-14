from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.billing import (
    get_create_billing_record_service,
    get_get_billing_record_service,
    get_list_billing_records_service,
    get_update_billing_record_service,
)
from app.schemas.billing import (
    BillingRecordCreate,
    BillingRecordListResponse,
    BillingRecordResponse,
    BillingRecordUpdate,
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

router = APIRouter(
    prefix="/organisations/{organisation_id}/billing",
    tags=["Billing"],
)


@router.post(
    "",
    response_model=BillingRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_billing_record(
    organisation_id: UUID,
    request: BillingRecordCreate,
    current_user: User = Depends(get_current_user),
    service: CreateBillingRecordService = Depends(
        get_create_billing_record_service,
    ),
):
    """Create a billing record for an organisation."""

    billing_record = await service.execute(
        organisation_id=organisation_id,
        user_id=current_user.id,
        subscription_id=request.subscription_id,
        customer_id=request.customer_id,
        plan_id=request.plan_id,
        billing_period_start=request.billing_period_start,
        billing_period_end=request.billing_period_end,
        amount=request.amount,
        currency=request.currency,
    )

    return BillingRecordResponse.model_validate(billing_record)


@router.get(
    "",
    response_model=BillingRecordListResponse,
)
async def list_billing_records(
    organisation_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ListBillingRecordsService = Depends(
        get_list_billing_records_service,
    ),
):
    """List billing records for an organisation."""

    billing_records = await service.execute(
        organisation_id=organisation_id,
        user_id=current_user.id,
    )

    return BillingRecordListResponse(
        items=[
            BillingRecordResponse.model_validate(record)
            for record in billing_records
        ],
        total=len(billing_records),
    )


@router.get(
    "/{billing_record_id}",
    response_model=BillingRecordResponse,
)
async def get_billing_record(
    organisation_id: UUID,
    billing_record_id: UUID,
    current_user: User = Depends(get_current_user),
    service: GetBillingRecordService = Depends(
        get_get_billing_record_service,
    ),
):
    """Get a billing record."""

    billing_record = await service.execute(
        billing_record_id=billing_record_id,
        organisation_id=organisation_id,
        user_id=current_user.id,
    )

    return BillingRecordResponse.model_validate(billing_record)


@router.patch(
    "/{billing_record_id}",
    response_model=BillingRecordResponse,
)
async def update_billing_record(
    organisation_id: UUID,
    billing_record_id: UUID,
    request: BillingRecordUpdate,
    current_user: User = Depends(get_current_user),
    service: UpdateBillingRecordService = Depends(
        get_update_billing_record_service,
    ),
):
    """Update a billing record."""

    billing_record = await service.execute(
        billing_record_id=billing_record_id,
        organisation_id=organisation_id,
        user_id=current_user.id,
        status=request.status,
    )

    return BillingRecordResponse.model_validate(billing_record)
