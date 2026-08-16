from decimal import Decimal

import pytest

from app.db.enums import PaymentStatus
from app.providers.payment.mock import MockPaymentProvider


@pytest.mark.asyncio
async def test_mock_create_payment():
    provider = MockPaymentProvider()

    result = await provider.create_payment(
        amount=Decimal("99.00"),
        currency="aud",
        payment_id="payment-123",
    )

    assert result.provider_payment_id == "mock_payment-123"
    assert result.status == PaymentStatus.PENDING
    assert result.amount == Decimal("99.00")
    assert result.currency == "AUD"


@pytest.mark.asyncio
async def test_mock_get_payment():
    provider = MockPaymentProvider()

    result = await provider.get_payment(
        provider_payment_id="mock_payment-123",
    )

    assert result.provider_payment_id == "mock_payment-123"
    assert result.status == PaymentStatus.PENDING


@pytest.mark.asyncio
async def test_mock_verify_payment():
    provider = MockPaymentProvider()

    result = await provider.verify_payment(
        provider_payment_id="mock_payment-123",
    )

    assert result.provider_payment_id == "mock_payment-123"
    assert result.status == PaymentStatus.SUCCEEDED


@pytest.mark.asyncio
async def test_mock_refund_payment():
    provider = MockPaymentProvider()

    result = await provider.refund_payment(
        provider_payment_id="mock_payment-123",
        amount=Decimal("50.00"),
    )

    assert result.provider_payment_id == "mock_payment-123"
    assert result.status == PaymentStatus.REFUNDED
    assert result.amount == Decimal("50.00")


@pytest.mark.asyncio
async def test_mock_webhook():
    provider = MockPaymentProvider()

    result = await provider.handle_webhook(
        payload=b"{}",
        signature="test-signature",
    )

    assert result.provider_payment_id == "mock_webhook_payment"
    assert result.status == PaymentStatus.SUCCEEDED
