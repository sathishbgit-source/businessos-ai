from decimal import Decimal

import pytest

from app.db.enums import PaymentStatus
from app.providers.payment.base import PaymentProvider
from app.providers.payment.models import PaymentProviderResult


class TestPaymentProvider(PaymentProvider):
    """Concrete implementation used to verify the provider contract."""

    async def create_payment(
        self,
        *,
        amount: Decimal,
        currency: str,
        payment_id: str,
    ) -> PaymentProviderResult:
        return PaymentProviderResult(
            provider_payment_id=payment_id,
            status=PaymentStatus.PENDING,
            amount=amount,
            currency=currency,
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
            provider_payment_id="webhook-payment",
            status=PaymentStatus.SUCCEEDED,
        )


def test_payment_provider_is_abstract():
    assert PaymentProvider.__abstractmethods__ == {
        "create_payment",
        "get_payment",
        "verify_payment",
        "refund_payment",
        "handle_webhook",
    }


def test_payment_provider_result():
    result = PaymentProviderResult(
        provider_payment_id="pay_test_123",
        status=PaymentStatus.SUCCEEDED,
        amount=Decimal("99.00"),
        currency="AUD",
    )

    assert result.provider_payment_id == "pay_test_123"
    assert result.status == PaymentStatus.SUCCEEDED
    assert result.amount == Decimal("99.00")
    assert result.currency == "AUD"


@pytest.mark.asyncio
async def test_payment_provider_contract():
    provider = TestPaymentProvider()

    result = await provider.create_payment(
        amount=Decimal("99.00"),
        currency="AUD",
        payment_id="payment-123",
    )

    assert result.provider_payment_id == "payment-123"
    assert result.status == PaymentStatus.PENDING
    assert result.amount == Decimal("99.00")
    assert result.currency == "AUD"
