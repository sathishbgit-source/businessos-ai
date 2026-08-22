from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    PaymentNotFound,
    PaymentStateTransitionDenied,
)
from app.db.enums import PaymentStatus
from app.db.models.payment import Payment
from app.providers.payment.models import PaymentProviderResult
from app.providers.payment.registry import PaymentProviderRegistry
from app.services.payment.handle_payment_webhook import (
    HandlePaymentWebhookService,
)


@pytest.fixture
def payment():
    return Payment(
        id=uuid4(),
        organisation_id=uuid4(),
        billing_record_id=uuid4(),
        subscription_id=uuid4(),
        customer_id=uuid4(),
        amount=Decimal("99.00"),
        currency="AUD",
        status=PaymentStatus.PROCESSING,
        provider="mock",
        provider_payment_id="mock_webhook_payment",
    )


@pytest.fixture
def provider():
    provider = AsyncMock()
    provider.handle_webhook.return_value = PaymentProviderResult(
        provider_payment_id="mock_webhook_payment",
        status=PaymentStatus.SUCCEEDED,
        amount=Decimal("99.00"),
        currency="AUD",
        paid_at=datetime.now(timezone.utc),
    )
    return provider


@pytest.fixture
def registry(provider):
    registry = PaymentProviderRegistry()
    registry.register("mock", lambda: provider)
    return registry


@pytest.fixture
def dunning_service():
    return AsyncMock()


@pytest.mark.asyncio
async def test_handle_payment_webhook_updates_payment(
    payment,
    provider,
    registry,
    dunning_service,
):
    repository = AsyncMock()
    repository.get_by_provider_payment_id.return_value = payment
    repository.update.return_value = payment

    db = AsyncMock()

    service = HandlePaymentWebhookService(
        db=db,
        payment_repository=repository,
        provider_registry=registry,
        dunning_service=dunning_service,
    )

    result = await service.execute(
        provider="MOCK",
        payload=b'{"event":"payment.succeeded"}',
        signature="test-signature",
    )

    assert result is payment
    assert payment.status == PaymentStatus.SUCCEEDED
    assert payment.paid_at is not None

    provider.handle_webhook.assert_awaited_once_with(
        payload=b'{"event":"payment.succeeded"}',
        signature="test-signature",
    )

    repository.get_by_provider_payment_id.assert_awaited_once_with(
        provider="mock",
        provider_payment_id="mock_webhook_payment",
    )
    repository.update.assert_awaited_once_with(payment)

    dunning_service.recover.assert_awaited_once_with(
        payment=payment,
    )
    dunning_service.start.assert_not_awaited()

    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(payment)


@pytest.mark.asyncio
async def test_handle_payment_webhook_starts_dunning_on_failure(
    payment,
    provider,
    registry,
    dunning_service,
):
    provider.handle_webhook.return_value = PaymentProviderResult(
        provider_payment_id="mock_webhook_payment",
        status=PaymentStatus.FAILED,
        amount=Decimal("99.00"),
        currency="AUD",
        failure_reason="card_declined",
    )

    repository = AsyncMock()
    repository.get_by_provider_payment_id.return_value = payment
    repository.update.return_value = payment

    db = AsyncMock()

    service = HandlePaymentWebhookService(
        db=db,
        payment_repository=repository,
        provider_registry=registry,
        dunning_service=dunning_service,
    )

    result = await service.execute(
        provider="mock",
        payload=b'{"event":"payment.failed"}',
        signature="test-signature",
    )

    assert result is payment
    assert payment.status == PaymentStatus.FAILED
    assert payment.failure_reason == "card_declined"

    dunning_service.start.assert_awaited_once()
    assert dunning_service.start.await_args.kwargs["payment"] is payment
    assert dunning_service.start.await_args.kwargs["now"] is not None

    dunning_service.recover.assert_not_awaited()

    repository.update.assert_awaited_once_with(payment)
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(payment)


@pytest.mark.asyncio
async def test_handle_payment_webhook_raises_when_payment_not_found(
    provider,
    registry,
    dunning_service,
):
    repository = AsyncMock()
    repository.get_by_provider_payment_id.return_value = None

    db = AsyncMock()

    service = HandlePaymentWebhookService(
        db=db,
        payment_repository=repository,
        provider_registry=registry,
        dunning_service=dunning_service,
    )

    with pytest.raises(
        PaymentNotFound,
        match="Payment referenced by webhook",
    ):
        await service.execute(
            provider="mock",
            payload=b"{}",
            signature="test-signature",
        )

    repository.update.assert_not_awaited()
    dunning_service.start.assert_not_awaited()
    dunning_service.recover.assert_not_awaited()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_handle_payment_webhook_rejects_invalid_transition(
    payment,
    provider,
    registry,
    dunning_service,
):
    payment.status = PaymentStatus.PENDING

    provider.handle_webhook.return_value = PaymentProviderResult(
        provider_payment_id="mock_webhook_payment",
        status=PaymentStatus.SUCCEEDED,
    )

    repository = AsyncMock()
    repository.get_by_provider_payment_id.return_value = payment

    db = AsyncMock()

    service = HandlePaymentWebhookService(
        db=db,
        payment_repository=repository,
        provider_registry=registry,
        dunning_service=dunning_service,
    )

    with pytest.raises(
        PaymentStateTransitionDenied,
        match="Payment cannot transition",
    ):
        await service.execute(
            provider="mock",
            payload=b"{}",
            signature="test-signature",
        )

    assert payment.status == PaymentStatus.PENDING
    repository.update.assert_not_awaited()
    dunning_service.start.assert_not_awaited()
    dunning_service.recover.assert_not_awaited()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_handle_payment_webhook_normalizes_provider_name(
    payment,
    provider,
    registry,
    dunning_service,
):
    repository = AsyncMock()
    repository.get_by_provider_payment_id.return_value = payment
    repository.update.return_value = payment

    db = AsyncMock()

    service = HandlePaymentWebhookService(
        db=db,
        payment_repository=repository,
        provider_registry=registry,
        dunning_service=dunning_service,
    )

    await service.execute(
        provider="  MOCK  ",
        payload=b"{}",
        signature="signature",
    )

    repository.get_by_provider_payment_id.assert_awaited_once_with(
        provider="mock",
        provider_payment_id="mock_webhook_payment",
    )
