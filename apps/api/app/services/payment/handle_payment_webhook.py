from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PaymentNotFound
from app.db.models.payment import Payment
from app.providers.payment.registry import PaymentProviderRegistry
from app.repositories.payment_repository import PaymentRepository
from app.services.payment.payment_state import PaymentStateService


class HandlePaymentWebhookService:
    """Apply a normalized payment-provider webhook to a payment."""

    def __init__(
        self,
        db: AsyncSession,
        payment_repository: PaymentRepository,
        provider_registry: PaymentProviderRegistry,
    ) -> None:
        self.db = db
        self.payment_repository = payment_repository
        self.provider_registry = provider_registry

    async def execute(
        self,
        *,
        provider: str,
        payload: bytes,
        signature: str,
    ) -> Payment:
        """Handle a provider webhook and update the payment."""

        payment_provider = self.provider_registry.get(provider)

        result = await payment_provider.handle_webhook(
            payload=payload,
            signature=signature,
        )

        payment = await self.payment_repository.get_by_provider_payment_id(
            provider=provider.strip().lower(),
            provider_payment_id=result.provider_payment_id,
        )

        if payment is None:
            raise PaymentNotFound(
                "Payment referenced by webhook does not exist."
            )

        PaymentStateService.validate_transition(
            current_status=payment.status,
            requested_status=result.status,
        )

        payment.status = result.status

        if result.failure_reason is not None:
            payment.failure_reason = result.failure_reason

        if result.paid_at is not None:
            payment.paid_at = result.paid_at

        payment = await self.payment_repository.update(payment)

        await self.db.commit()
        await self.db.refresh(payment)

        return payment
