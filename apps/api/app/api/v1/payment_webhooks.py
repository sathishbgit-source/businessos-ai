from fastapi import APIRouter, Depends, Header, Request

from app.dependencies.payment import get_handle_payment_webhook_service
from app.schemas.payment import PaymentResponse
from app.services.payment.handle_payment_webhook import (
    HandlePaymentWebhookService,
)


router = APIRouter(
    prefix="/payments/webhooks",
    tags=["Payment Webhooks"],
)


@router.post(
    "/{provider}",
    response_model=PaymentResponse,
)
async def handle_payment_webhook(
    provider: str,
    request: Request,
    signature: str = Header(..., alias="X-Payment-Signature"),
    service: HandlePaymentWebhookService = Depends(
        get_handle_payment_webhook_service,
    ),
):
    """Handle an external payment-provider webhook."""

    payload = await request.body()

    payment = await service.execute(
        provider=provider,
        payload=payload,
        signature=signature,
    )

    return PaymentResponse.model_validate(payment)
