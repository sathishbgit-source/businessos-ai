from uuid import UUID

from fastapi import APIRouter, Depends

from app.db.enums import PaymentStatus
from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.payment import (
    get_create_payment_service,
    get_get_payment_service,
    get_list_payments_service,
    get_update_payment_service,
)
from app.schemas.payment import (
    PaymentCreate,
    PaymentListResponse,
    PaymentResponse,
    PaymentUpdate,
)
from app.services.payment.create_payment import CreatePaymentService
from app.services.payment.get_payment import GetPaymentService
from app.services.payment.list_payments import ListPaymentsService
from app.services.payment.update_payment import UpdatePaymentService


router = APIRouter(
    prefix="/organisations/{organisation_id}/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=201,
)
async def create_payment(
    organisation_id: UUID,
    request: PaymentCreate,
    current_user: User = Depends(get_current_user),
    service: CreatePaymentService = Depends(
        get_create_payment_service,
    ),
):
    """Create a payment for an organisation."""

    payment = await service.execute(
        organisation_id=organisation_id,
        user_id=current_user.id,
        billing_record_id=request.billing_record_id,
        subscription_id=request.subscription_id,
        customer_id=request.customer_id,
        amount=request.amount,
        currency=request.currency,
        provider=request.provider,
        provider_payment_id=request.provider_payment_id,
    )

    return PaymentResponse.model_validate(payment)


@router.get(
    "",
    response_model=PaymentListResponse,
)
async def list_payments(
    organisation_id: UUID,
    status: PaymentStatus | None = None,
    current_user: User = Depends(get_current_user),
    service: ListPaymentsService = Depends(
        get_list_payments_service,
    ),
):
    """List payments for an organisation."""

    payments = await service.execute(
        organisation_id=organisation_id,
        user_id=current_user.id,
        status=status,
    )

    return PaymentListResponse(
        items=[
            PaymentResponse.model_validate(payment)
            for payment in payments
        ],
        total=len(payments),
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
async def get_payment(
    organisation_id: UUID,
    payment_id: UUID,
    current_user: User = Depends(get_current_user),
    service: GetPaymentService = Depends(
        get_get_payment_service,
    ),
):
    """Get a payment."""

    payment = await service.execute(
        payment_id=payment_id,
        organisation_id=organisation_id,
        user_id=current_user.id,
    )

    return PaymentResponse.model_validate(payment)


@router.patch(
    "/{payment_id}",
    response_model=PaymentResponse,
)
async def update_payment(
    organisation_id: UUID,
    payment_id: UUID,
    request: PaymentUpdate,
    current_user: User = Depends(get_current_user),
    service: UpdatePaymentService = Depends(
        get_update_payment_service,
    ),
):
    """Update a payment."""

    payment = await service.execute(
        payment_id=payment_id,
        organisation_id=organisation_id,
        user_id=current_user.id,
        status=request.status,
        provider_payment_id=request.provider_payment_id,
        failure_reason=request.failure_reason,
        paid_at=request.paid_at,
    )

    return PaymentResponse.model_validate(payment)
