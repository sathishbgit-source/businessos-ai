from decimal import Decimal

from app.db.enums import PaymentStatus
from app.providers.payment.base import PaymentProvider
from app.providers.payment.models import PaymentProviderResult


class MockPaymentProvider(PaymentProvider):
    """Deterministic provider used for local development and testing."""

    async def create_payment(
        self,
        *,
        amount: Decimal,
        currency: str,
        payment_id: str,
    ) -> PaymentProviderResult:
        return PaymentProviderResult(
            provider_payment_id=f"mock_{payment_id}",
            status=PaymentStatus.PENDING,
            amount=amount,
            currency=currency.upper(),
        )

    async def get_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> PaymentProviderResult:
        return PaymentProviderResult(
            provider_payment_id=provider_payment_id,
            status=PaymentStatus.PENDING,
        )

    async def verify_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> PaymentProviderResult:
        return PaymentProviderResult(
            provider_payment_id=provider_payment_id,
            status=PaymentStatus.SUCCEEDED,
        )

    async def refund_payment(
        self,
        *,
        provider_payment_id: str,
        amount: Decimal | None = None,
    ) -> PaymentProviderResult:
        return PaymentProviderResult(
            provider_payment_id=provider_payment_id,
            status=PaymentStatus.REFUNDED,
            amount=amount,
        )

    async def handle_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> PaymentProviderResult:
        return PaymentProviderResult(
            provider_payment_id="mock_webhook_payment",
            status=PaymentStatus.SUCCEEDED,
        )
