from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.v1.router import router as api_v1_router
from app.core.exceptions import (
    PaymentAccessDenied,
    PaymentCustomerMismatch,
    PaymentNotFound,
    PaymentProviderReferenceAlreadyExists,
    PaymentStateTransitionDenied,
)
from app.db.enums import PaymentStatus
from app.db.models.payment import Payment
from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.payment import (
    get_create_payment_service,
    get_get_payment_service,
    get_list_payments_service,
    get_update_payment_service,
)
from app.main import app


@pytest.fixture
def organisation_id():
    return uuid4()


@pytest.fixture
def user():
    return User(
        id=uuid4(),
    )


@pytest.fixture
def payment(organisation_id):
    now = datetime.now(timezone.utc)

    return Payment(
        id=uuid4(),
        organisation_id=organisation_id,
        billing_record_id=uuid4(),
        subscription_id=uuid4(),
        customer_id=uuid4(),
        amount=Decimal("99.00"),
        currency="AUD",
        status=PaymentStatus.PENDING,
        provider="test",
        provider_payment_id=None,
        failure_reason=None,
        paid_at=None,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def client(user):
    async def override_current_user():
        return user

    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_payment_returns_201(
    client,
    user,
    payment,
    organisation_id,
):
    service = AsyncMock()
    service.execute.return_value = payment

    async def override_service():
        return service

    app.dependency_overrides[
        get_create_payment_service
    ] = override_service

    payload = {
        "billing_record_id": str(payment.billing_record_id),
        "subscription_id": str(payment.subscription_id),
        "customer_id": str(payment.customer_id),
        "amount": "99.00",
        "currency": "AUD",
        "provider": "test",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == str(payment.id)
    assert data["organisation_id"] == str(organisation_id)
    assert data["amount"] == "99.00"
    assert data["currency"] == "AUD"
    assert data["status"] == PaymentStatus.PENDING.value
    assert data["provider"] == "test"

    service.execute.assert_awaited_once_with(
        organisation_id=organisation_id,
        user_id=user.id,
        billing_record_id=payment.billing_record_id,
        subscription_id=payment.subscription_id,
        customer_id=payment.customer_id,
        amount=Decimal("99.00"),
        currency="AUD",
        provider="test",
        provider_payment_id=None,
    )

    app.dependency_overrides.pop(
        get_create_payment_service,
        None,
    )


def test_list_payments_returns_200(
    client,
    user,
    payment,
    organisation_id,
):
    service = AsyncMock()
    service.execute.return_value = [payment]

    async def override_service():
        return service

    app.dependency_overrides[
        get_list_payments_service
    ] = override_service

    response = client.get(
        f"/api/v1/organisations/{organisation_id}/payments",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(payment.id)

    service.execute.assert_awaited_once_with(
        organisation_id=organisation_id,
        user_id=user.id,
        status=None,
    )

    app.dependency_overrides.pop(
        get_list_payments_service,
        None,
    )


def test_list_payments_supports_status_filter(
    client,
    user,
    payment,
    organisation_id,
):
    service = AsyncMock()
    service.execute.return_value = [payment]

    async def override_service():
        return service

    app.dependency_overrides[
        get_list_payments_service
    ] = override_service

    response = client.get(
        f"/api/v1/organisations/{organisation_id}/payments",
        params={"status": PaymentStatus.PENDING.value},
    )

    assert response.status_code == 200

    service.execute.assert_awaited_once_with(
        organisation_id=organisation_id,
        user_id=user.id,
        status=PaymentStatus.PENDING,
    )

    app.dependency_overrides.pop(
        get_list_payments_service,
        None,
    )


def test_get_payment_returns_200(
    client,
    user,
    payment,
    organisation_id,
):
    service = AsyncMock()
    service.execute.return_value = payment

    async def override_service():
        return service

    app.dependency_overrides[
        get_get_payment_service
    ] = override_service

    response = client.get(
        f"/api/v1/organisations/{organisation_id}/payments/{payment.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(payment.id)
    assert data["organisation_id"] == str(organisation_id)

    service.execute.assert_awaited_once_with(
        payment_id=payment.id,
        organisation_id=organisation_id,
        user_id=user.id,
    )

    app.dependency_overrides.pop(
        get_get_payment_service,
        None,
    )


def test_update_payment_returns_200(
    client,
    user,
    payment,
    organisation_id,
):
    payment.status = PaymentStatus.SUCCEEDED

    service = AsyncMock()
    service.execute.return_value = payment

    async def override_service():
        return service

    app.dependency_overrides[
        get_update_payment_service
    ] = override_service

    payload = {
        "status": PaymentStatus.SUCCEEDED.value,
    }

    response = client.patch(
        f"/api/v1/organisations/{organisation_id}/payments/{payment.id}",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(payment.id)
    assert data["status"] == PaymentStatus.SUCCEEDED.value

    service.execute.assert_awaited_once_with(
        payment_id=payment.id,
        organisation_id=organisation_id,
        user_id=user.id,
        status=PaymentStatus.SUCCEEDED,
        provider_payment_id=None,
        failure_reason=None,
        paid_at=None,
    )

    app.dependency_overrides.pop(
        get_update_payment_service,
        None,
    )


def test_update_payment_rejects_invalid_status_transition(
    client,
    user,
    payment,
    organisation_id,
):
    service = AsyncMock()
    service.execute.side_effect = PaymentStateTransitionDenied(
        "Payment cannot transition from 'PENDING' to 'SUCCEEDED'."
    )

    async def override_service():
        return service

    app.dependency_overrides[
        get_update_payment_service
    ] = override_service

    payload = {
        "status": PaymentStatus.SUCCEEDED.value,
    }

    response = client.patch(
        f"/api/v1/organisations/{organisation_id}/payments/{payment.id}",
        json=payload,
    )

    assert response.status_code == 409

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == (
        "PAYMENT_STATE_TRANSITION_DENIED"
    )

    service.execute.assert_awaited_once_with(
        payment_id=payment.id,
        organisation_id=organisation_id,
        user_id=user.id,
        status=PaymentStatus.SUCCEEDED,
        provider_payment_id=None,
        failure_reason=None,
        paid_at=None,
    )

    app.dependency_overrides.pop(
        get_update_payment_service,
        None,
    )


def test_create_payment_requires_authentication(
    payment,
    organisation_id,
):
    with TestClient(app) as test_client:
        payload = {
            "billing_record_id": str(payment.billing_record_id),
            "subscription_id": str(payment.subscription_id),
            "customer_id": str(payment.customer_id),
            "amount": "99.00",
            "currency": "AUD",
            "provider": "test",
        }

        response = test_client.post(
            f"/api/v1/organisations/{organisation_id}/payments",
            json=payload,
        )

    assert response.status_code == 401


def test_get_payment_returns_404_when_service_raises_not_found(
    client,
    organisation_id,
):
    service = AsyncMock()
    service.execute.side_effect = PaymentNotFound(
        "Payment not found",
    )

    async def override_service():
        return service

    app.dependency_overrides[
        get_get_payment_service
    ] = override_service

    payment_id = uuid4()

    response = client.get(
        f"/api/v1/organisations/{organisation_id}/payments/{payment_id}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "PAYMENT_NOT_FOUND"

    app.dependency_overrides.pop(
        get_get_payment_service,
        None,
    )


def test_get_payment_returns_403_when_service_denies_access(
    client,
    organisation_id,
):
    service = AsyncMock()
    service.execute.side_effect = PaymentAccessDenied(
        "Payment access denied",
    )

    async def override_service():
        return service

    app.dependency_overrides[
        get_get_payment_service
    ] = override_service

    payment_id = uuid4()

    response = client.get(
        f"/api/v1/organisations/{organisation_id}/payments/{payment_id}",
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "PAYMENT_ACCESS_DENIED"

    app.dependency_overrides.pop(
        get_get_payment_service,
        None,
    )


def test_create_payment_validates_request(
    client,
    organisation_id,
):
    payload = {
        "billing_record_id": "not-a-uuid",
        "subscription_id": str(uuid4()),
        "customer_id": str(uuid4()),
        "amount": "99.00",
        "currency": "AUD",
        "provider": "test",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_payment_rejects_non_positive_amount(
    client,
    organisation_id,
):
    payload = {
        "billing_record_id": str(uuid4()),
        "subscription_id": str(uuid4()),
        "customer_id": str(uuid4()),
        "amount": "0.00",
        "currency": "AUD",
        "provider": "test",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_payment_rejects_negative_amount(
    client,
    organisation_id,
):
    payload = {
        "billing_record_id": str(uuid4()),
        "subscription_id": str(uuid4()),
        "customer_id": str(uuid4()),
        "amount": "-1.00",
        "currency": "AUD",
        "provider": "test",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.parametrize(
    "currency",
    [
        "AU",
        "AUDD",
        "12$",
    ],
)
def test_create_payment_rejects_invalid_currency(
    client,
    organisation_id,
    currency,
):
    payload = {
        "billing_record_id": str(uuid4()),
        "subscription_id": str(uuid4()),
        "customer_id": str(uuid4()),
        "amount": "99.00",
        "currency": currency,
        "provider": "test",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_payment_rejects_empty_provider(
    client,
    organisation_id,
):
    payload = {
        "billing_record_id": str(uuid4()),
        "subscription_id": str(uuid4()),
        "customer_id": str(uuid4()),
        "amount": "99.00",
        "currency": "AUD",
        "provider": "",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_payment_returns_400_for_customer_mismatch(
    client,
    organisation_id,
):
    service = AsyncMock()
    service.execute.side_effect = PaymentCustomerMismatch(
        "Payment customer does not match the subscription customer.",
    )

    async def override_service():
        return service

    app.dependency_overrides[
        get_create_payment_service
    ] = override_service

    payload = {
        "billing_record_id": str(uuid4()),
        "subscription_id": str(uuid4()),
        "customer_id": str(uuid4()),
        "amount": "99.00",
        "currency": "AUD",
        "provider": "test",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "PAYMENT_CUSTOMER_MISMATCH"

    app.dependency_overrides.pop(
        get_create_payment_service,
        None,
    )


def test_create_payment_returns_409_for_duplicate_provider_reference(
    client,
    organisation_id,
):
    service = AsyncMock()
    service.execute.side_effect = PaymentProviderReferenceAlreadyExists(
        "A payment already exists for this provider payment reference.",
    )

    async def override_service():
        return service

    app.dependency_overrides[
        get_create_payment_service
    ] = override_service

    payload = {
        "billing_record_id": str(uuid4()),
        "subscription_id": str(uuid4()),
        "customer_id": str(uuid4()),
        "amount": "99.00",
        "currency": "AUD",
        "provider": "stripe",
        "provider_payment_id": "pi_123",
    }

    response = client.post(
        f"/api/v1/organisations/{organisation_id}/payments",
        json=payload,
    )

    assert response.status_code == 409

    data = response.json()

    assert data["success"] is False
    assert (
        data["error"]["code"]
        == "PAYMENT_PROVIDER_REFERENCE_ALREADY_EXISTS"
    )

    app.dependency_overrides.pop(
        get_create_payment_service,
        None,
    )
