from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.dependencies.payment import get_handle_payment_webhook_service
from app.db.enums import PaymentStatus
from app.db.models.payment import Payment
from app.main import app


def make_payment() -> Payment:
    now = datetime.now(timezone.utc)

    return Payment(
        id=uuid4(),
        organisation_id=uuid4(),
        billing_record_id=uuid4(),
        subscription_id=uuid4(),
        customer_id=uuid4(),
        amount=Decimal("99.00"),
        currency="AUD",
        status=PaymentStatus.SUCCEEDED,
        provider="mock",
        provider_payment_id="mock_webhook_payment",
        failure_reason=None,
        paid_at=now,
        created_at=now,
        updated_at=now,
    )


def test_payment_webhook_accepts_raw_payload_and_signature():
    service = AsyncMock()
    payment = make_payment()
    service.execute.return_value = payment

    async def override_service():
        return service

    app.dependency_overrides[
        get_handle_payment_webhook_service
    ] = override_service

    payload = b'{"event":"payment.succeeded","amount":9900}'
    signature = "test-signature"

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/payments/webhooks/mock",
                content=payload,
                headers={
                    "X-Payment-Signature": signature,
                    "Content-Type": "application/json",
                },
            )

        assert response.status_code == 200

        service.execute.assert_awaited_once_with(
            provider="mock",
            payload=payload,
            signature=signature,
        )

        data = response.json()
        assert data["id"] == str(payment.id)
        assert data["status"] == PaymentStatus.SUCCEEDED.value
        assert data["provider"] == "mock"
        assert data["provider_payment_id"] == (
            "mock_webhook_payment"
        )
    finally:
        app.dependency_overrides.pop(
            get_handle_payment_webhook_service,
            None,
        )


def test_payment_webhook_does_not_require_authentication():
    service = AsyncMock()
    payment = make_payment()
    service.execute.return_value = payment

    async def override_service():
        return service

    app.dependency_overrides[
        get_handle_payment_webhook_service
    ] = override_service

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/payments/webhooks/mock",
                content=b"{}",
                headers={
                    "X-Payment-Signature": "signature",
                },
            )

        assert response.status_code == 200
    finally:
        app.dependency_overrides.pop(
            get_handle_payment_webhook_service,
            None,
        )


def test_payment_webhook_requires_signature():
    service = AsyncMock()

    async def override_service():
        return service

    app.dependency_overrides[
        get_handle_payment_webhook_service
    ] = override_service

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/payments/webhooks/mock",
                content=b"{}",
            )

        assert response.status_code == 422
        service.execute.assert_not_awaited()
    finally:
        app.dependency_overrides.pop(
            get_handle_payment_webhook_service,
            None,
        )
