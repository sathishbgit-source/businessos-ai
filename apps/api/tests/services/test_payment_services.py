from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    BillingRecordNotFound,
    OrganisationAccessDenied,
    PaymentAccessDenied,
    PaymentCustomerMismatch,
    PaymentNotFound,
    PaymentProviderReferenceAlreadyExists,
    PaymentStateTransitionDenied,
    SubscriptionNotFound,
)
from app.db.enums import MemberStatus, PaymentStatus
from app.db.models.payment import Payment
from app.services.payment.create_payment import CreatePaymentService
from app.services.payment.get_payment import GetPaymentService
from app.services.payment.list_payments import ListPaymentsService
from app.services.payment.update_payment import UpdatePaymentService


@pytest.fixture
def payment():
    organisation_id = uuid4()

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
    )


@pytest.fixture
def active_member():
    member = AsyncMock()
    member.status = MemberStatus.ACTIVE
    return member


@pytest.mark.asyncio
async def test_get_payment_returns_payment(payment, active_member):
    repository = AsyncMock()
    repository.get_by_id.return_value = payment

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = GetPaymentService(
        db=AsyncMock(),
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    result = await service.execute(
        payment_id=payment.id,
        organisation_id=payment.organisation_id,
        user_id=uuid4(),
    )

    assert result is payment
    repository.get_by_id.assert_awaited_once_with(payment.id)


@pytest.mark.asyncio
async def test_get_payment_raises_when_not_found():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    organisation_repository = AsyncMock()

    service = GetPaymentService(
        db=AsyncMock(),
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    with pytest.raises(PaymentNotFound):
        await service.execute(
            payment_id=uuid4(),
            organisation_id=uuid4(),
            user_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_get_payment_denies_wrong_organisation(payment):
    repository = AsyncMock()
    repository.get_by_id.return_value = payment

    organisation_repository = AsyncMock()

    service = GetPaymentService(
        db=AsyncMock(),
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    with pytest.raises(PaymentAccessDenied):
        await service.execute(
            payment_id=payment.id,
            organisation_id=uuid4(),
            user_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_list_payments_by_organisation(payment, active_member):
    repository = AsyncMock()
    repository.get_all_by_organisation.return_value = [payment]

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = ListPaymentsService(
        db=AsyncMock(),
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    result = await service.execute(
        organisation_id=payment.organisation_id,
        user_id=uuid4(),
    )

    assert result == [payment]

    repository.get_all_by_organisation.assert_awaited_once_with(
        organisation_id=payment.organisation_id,
    )


@pytest.mark.asyncio
async def test_list_payments_by_status(payment, active_member):
    repository = AsyncMock()
    repository.get_all_by_organisation_and_status.return_value = [payment]

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = ListPaymentsService(
        db=AsyncMock(),
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    result = await service.execute(
        organisation_id=payment.organisation_id,
        user_id=uuid4(),
        status=PaymentStatus.PENDING,
    )

    assert result == [payment]

    repository.get_all_by_organisation_and_status.assert_awaited_once_with(
        organisation_id=payment.organisation_id,
        status=PaymentStatus.PENDING,
    )


@pytest.mark.asyncio
async def test_list_payments_denies_inactive_member(payment):
    repository = AsyncMock()

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = None

    service = ListPaymentsService(
        db=AsyncMock(),
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    with pytest.raises(PaymentAccessDenied):
        await service.execute(
            organisation_id=payment.organisation_id,
            user_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_update_payment_status(payment, active_member):
    repository = AsyncMock()
    repository.get_by_id.return_value = payment
    repository.update.return_value = payment

    db = AsyncMock()

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = UpdatePaymentService(
        db=db,
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    result = await service.execute(
        payment_id=payment.id,
        organisation_id=payment.organisation_id,
        user_id=uuid4(),
        status=PaymentStatus.PROCESSING,
    )

    assert result is payment
    assert payment.status == PaymentStatus.PROCESSING

    repository.update.assert_awaited_once_with(payment)
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("current_status", "requested_status"),
    [
        (PaymentStatus.PENDING, PaymentStatus.CANCELLED),
        (PaymentStatus.PROCESSING, PaymentStatus.SUCCEEDED),
        (PaymentStatus.PROCESSING, PaymentStatus.FAILED),
        (PaymentStatus.SUCCEEDED, PaymentStatus.REFUNDED),
    ],
)
async def test_update_payment_allows_valid_status_transitions(
    payment,
    active_member,
    current_status,
    requested_status,
):
    payment.status = current_status

    repository = AsyncMock()
    repository.get_by_id.return_value = payment
    repository.update.return_value = payment

    db = AsyncMock()

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = UpdatePaymentService(
        db=db,
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    result = await service.execute(
        payment_id=payment.id,
        organisation_id=payment.organisation_id,
        user_id=uuid4(),
        status=requested_status,
    )

    assert result is payment
    assert payment.status == requested_status

    repository.update.assert_awaited_once_with(payment)
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("current_status", "requested_status"),
    [
        (PaymentStatus.PENDING, PaymentStatus.SUCCEEDED),
        (PaymentStatus.PENDING, PaymentStatus.FAILED),
        (PaymentStatus.PENDING, PaymentStatus.REFUNDED),
        (PaymentStatus.PROCESSING, PaymentStatus.CANCELLED),
        (PaymentStatus.SUCCEEDED, PaymentStatus.PENDING),
        (PaymentStatus.SUCCEEDED, PaymentStatus.FAILED),
        (PaymentStatus.FAILED, PaymentStatus.SUCCEEDED),
        (PaymentStatus.CANCELLED, PaymentStatus.PROCESSING),
        (PaymentStatus.REFUNDED, PaymentStatus.SUCCEEDED),
    ],
)
async def test_update_payment_rejects_invalid_status_transitions(
    payment,
    active_member,
    current_status,
    requested_status,
):
    payment.status = current_status

    repository = AsyncMock()
    repository.get_by_id.return_value = payment

    db = AsyncMock()

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = UpdatePaymentService(
        db=db,
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    with pytest.raises(
        PaymentStateTransitionDenied,
        match="Payment cannot transition",
    ):
        await service.execute(
            payment_id=payment.id,
            organisation_id=payment.organisation_id,
            user_id=uuid4(),
            status=requested_status,
        )

    assert payment.status == current_status
    repository.update.assert_not_awaited()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_payment_raises_when_not_found():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    organisation_repository = AsyncMock()

    service = UpdatePaymentService(
        db=AsyncMock(),
        payment_repository=repository,
        organisation_member_repository=organisation_repository,
    )

    with pytest.raises(PaymentNotFound):
        await service.execute(
            payment_id=uuid4(),
            organisation_id=uuid4(),
            user_id=uuid4(),
            status=PaymentStatus.SUCCEEDED,
        )


@pytest.mark.asyncio
async def test_create_payment_success(payment, active_member):
    payment_repository = AsyncMock()
    payment_repository.create.return_value = payment
    payment_repository.get_by_provider_payment_id.return_value = None

    billing_repository = AsyncMock()
    billing_record = AsyncMock()
    billing_record.organisation_id = payment.organisation_id
    billing_repository.get_by_id.return_value = billing_record

    subscription_repository = AsyncMock()
    subscription = AsyncMock()
    subscription.organisation_id = payment.organisation_id
    subscription.customer_id = payment.customer_id
    subscription_repository.get_by_id.return_value = subscription

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    db = AsyncMock()

    service = CreatePaymentService(
        db=db,
        payment_repository=payment_repository,
        organisation_member_repository=organisation_repository,
        billing_repository=billing_repository,
        subscription_repository=subscription_repository,
    )

    result = await service.execute(
        organisation_id=payment.organisation_id,
        user_id=uuid4(),
        billing_record_id=payment.billing_record_id,
        subscription_id=payment.subscription_id,
        customer_id=payment.customer_id,
        amount=Decimal("99.00"),
        currency="aud",
        provider="test",
    )

    assert result is payment
    payment_repository.create.assert_awaited_once()
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_payment_rejects_duplicate_provider_reference(
    payment,
    active_member,
):
    provider_payment_id = "provider-payment-123"

    payment_repository = AsyncMock()
    payment_repository.get_by_provider_payment_id.return_value = payment

    billing_repository = AsyncMock()
    billing_record = AsyncMock()
    billing_record.organisation_id = payment.organisation_id
    billing_repository.get_by_id.return_value = billing_record

    subscription_repository = AsyncMock()
    subscription = AsyncMock()
    subscription.organisation_id = payment.organisation_id
    subscription.customer_id = payment.customer_id
    subscription_repository.get_by_id.return_value = subscription

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    db = AsyncMock()

    service = CreatePaymentService(
        db=db,
        payment_repository=payment_repository,
        organisation_member_repository=organisation_repository,
        billing_repository=billing_repository,
        subscription_repository=subscription_repository,
    )

    with pytest.raises(
        PaymentProviderReferenceAlreadyExists,
        match="provider payment reference",
    ):
        await service.execute(
            organisation_id=payment.organisation_id,
            user_id=uuid4(),
            billing_record_id=payment.billing_record_id,
            subscription_id=payment.subscription_id,
            customer_id=payment.customer_id,
            amount=Decimal("99.00"),
            currency="AUD",
            provider="test",
            provider_payment_id=provider_payment_id,
        )

    payment_repository.get_by_provider_payment_id.assert_awaited_once_with(
        provider="test",
        provider_payment_id=provider_payment_id,
    )
    payment_repository.create.assert_not_awaited()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_payment_rejects_missing_billing_record(
    payment,
    active_member,
):
    payment_repository = AsyncMock()

    billing_repository = AsyncMock()
    billing_repository.get_by_id.return_value = None

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = CreatePaymentService(
        db=AsyncMock(),
        payment_repository=payment_repository,
        organisation_member_repository=organisation_repository,
        billing_repository=billing_repository,
        subscription_repository=AsyncMock(),
    )

    with pytest.raises(BillingRecordNotFound):
        await service.execute(
            organisation_id=payment.organisation_id,
            user_id=uuid4(),
            billing_record_id=payment.billing_record_id,
            subscription_id=payment.subscription_id,
            customer_id=payment.customer_id,
            amount=Decimal("99.00"),
            currency="AUD",
            provider="test",
        )


@pytest.mark.asyncio
async def test_create_payment_rejects_wrong_billing_record_organisation(
    payment,
    active_member,
):
    payment_repository = AsyncMock()

    billing_repository = AsyncMock()
    billing_record = AsyncMock()
    billing_record.organisation_id = uuid4()
    billing_repository.get_by_id.return_value = billing_record

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = CreatePaymentService(
        db=AsyncMock(),
        payment_repository=payment_repository,
        organisation_member_repository=organisation_repository,
        billing_repository=billing_repository,
        subscription_repository=AsyncMock(),
    )

    with pytest.raises(OrganisationAccessDenied):
        await service.execute(
            organisation_id=payment.organisation_id,
            user_id=uuid4(),
            billing_record_id=payment.billing_record_id,
            subscription_id=payment.subscription_id,
            customer_id=payment.customer_id,
            amount=Decimal("99.00"),
            currency="AUD",
            provider="test",
        )


@pytest.mark.asyncio
async def test_create_payment_rejects_missing_subscription(
    payment,
    active_member,
):
    payment_repository = AsyncMock()

    billing_repository = AsyncMock()
    billing_record = AsyncMock()
    billing_record.organisation_id = payment.organisation_id
    billing_repository.get_by_id.return_value = billing_record

    subscription_repository = AsyncMock()
    subscription_repository.get_by_id.return_value = None

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = CreatePaymentService(
        db=AsyncMock(),
        payment_repository=payment_repository,
        organisation_member_repository=organisation_repository,
        billing_repository=billing_repository,
        subscription_repository=subscription_repository,
    )

    with pytest.raises(SubscriptionNotFound):
        await service.execute(
            organisation_id=payment.organisation_id,
            user_id=uuid4(),
            billing_record_id=payment.billing_record_id,
            subscription_id=payment.subscription_id,
            customer_id=payment.customer_id,
            amount=Decimal("99.00"),
            currency="AUD",
            provider="test",
        )


@pytest.mark.asyncio
async def test_create_payment_rejects_customer_mismatch(
    payment,
    active_member,
):
    payment_repository = AsyncMock()

    billing_repository = AsyncMock()
    billing_record = AsyncMock()
    billing_record.organisation_id = payment.organisation_id
    billing_repository.get_by_id.return_value = billing_record

    subscription_repository = AsyncMock()
    subscription = AsyncMock()
    subscription.organisation_id = payment.organisation_id
    subscription.customer_id = uuid4()
    subscription_repository.get_by_id.return_value = subscription

    organisation_repository = AsyncMock()
    organisation_repository.get_by_organisation_and_user.return_value = (
        active_member
    )

    service = CreatePaymentService(
        db=AsyncMock(),
        payment_repository=payment_repository,
        organisation_member_repository=organisation_repository,
        billing_repository=billing_repository,
        subscription_repository=subscription_repository,
    )

    with pytest.raises(
        PaymentCustomerMismatch,
        match="customer",
    ):
        await service.execute(
            organisation_id=payment.organisation_id,
            user_id=uuid4(),
            billing_record_id=payment.billing_record_id,
            subscription_id=payment.subscription_id,
            customer_id=payment.customer_id,
            amount=Decimal("99.00"),
            currency="AUD",
            provider="test",
        )
