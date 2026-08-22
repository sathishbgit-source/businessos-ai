from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PaymentNotFound
from app.db.enums import PaymentStatus
from app.db.models.payment import Payment
from app.providers.payment.registry import PaymentProviderRegistry
from app.repositories.payment_repository import PaymentRepository
from app.services.dunning.dunning_service import DunningService
from app.services.payment.payment_state import PaymentStateService


class HandlePaymentWebhookService:
    """Apply a normalized payment-provider webhook to a payment."""

    def __init__(
        self,
        db: AsyncSession,
        payment_repository: PaymentRepository,
        provider_registry: PaymentProviderRegistry,
        dunning_service: DunningService,
    ) -> None:
        self.db = db
        self.payment_repository = payment_repository
        self.provider_registry = provider_registry
        self.dunning_service = dunning_service

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

        normalized_provider = provider.strip().lower()

        payment = await self.payment_repository.get_by_provider_payment_id(
            provider=normalized_provider,
            provider_payment_id=result.provider_payment_id,
        )

        if payment is None:
            raise PaymentNotFound(
                "Payment referenced by webhook does not exist."
            )

        previous_status = payment.status

        PaymentStateService.validate_transition(
            current_status=previous_status,
            requested_status=result.status,
        )

        payment.status = result.status

        if result.failure_reason is not None:
            payment.failure_reason = result.failure_reason

        if result.paid_at is not None:
            payment.paid_at = result.paid_at

        payment = await self.payment_repository.update(payment)

        if result.status == PaymentStatus.FAILED:
            from datetime import datetime, timezone

            await self.dunning_service.start(
                payment=payment,
                now=datetime.now(timezone.utc),
            )

        elif result.status == PaymentStatus.SUCCEEDED:
            await self.dunning_service.recover(
                payment=payment,
            )

        await self.db.commit()
        await self.db.refresh(payment)

        return payment
