from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.db.enums import BillingStatus, DunningStatus
from app.db.enums import PaymentStatus, SubscriptionStatus
from app.db.models.billing_record import BillingRecord
from app.db.models.dunning import DunningRecord
from app.db.models.payment import Payment
from app.db.models.subscription import Subscription
from app.providers.payment.models import PaymentProviderResult
from app.providers.payment.registry import PaymentProviderRegistry
from app.services.dunning.dunning_policy import DunningPolicy
from app.services.dunning.dunning_service import DunningService


@pytest.fixture
def now():
    return datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)


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
        status=PaymentStatus.FAILED,
        provider="mock",
        provider_payment_id="failed-payment",
        failure_reason="card_declined",
    )


@pytest.fixture
def billing_record(payment):
    return BillingRecord(
        id=payment.billing_record_id,
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        customer_id=payment.customer_id,
        plan_id=uuid4(),
        billing_period_start=datetime(
            2026,
            8,
            1,
            tzinfo=timezone.utc,
        ),
        billing_period_end=datetime(
            2026,
            9,
            1,
            tzinfo=timezone.utc,
        ),
        amount=Decimal("99.00"),
        currency="AUD",
        status=BillingStatus.PENDING,
    )


@pytest.fixture
def subscription(payment):
    return Subscription(
        id=payment.subscription_id,
        organisation_id=payment.organisation_id,
        customer_id=payment.customer_id,
        plan_id=uuid4(),
        status=SubscriptionStatus.ACTIVE,
        current_period_start=datetime(
            2026,
            8,
            1,
            tzinfo=timezone.utc,
        ),
        current_period_end=datetime(
            2026,
            9,
            1,
            tzinfo=timezone.utc,
        ),
    )


@pytest.fixture
def repositories():
    return {
        "dunning": AsyncMock(),
        "payment": AsyncMock(),
        "billing": AsyncMock(),
        "subscription": AsyncMock(),
    }


@pytest.fixture
def provider_registry():
    provider = AsyncMock()
    provider.create_payment.return_value = PaymentProviderResult(
        provider_payment_id="retry-payment",
        status=PaymentStatus.PENDING,
        amount=Decimal("99.00"),
        currency="AUD",
    )

    registry = PaymentProviderRegistry()
    registry.register("mock", lambda: provider)

    return registry, provider


def build_service(repositories, provider_registry):
    registry, _ = provider_registry

    return DunningService(
        db=AsyncMock(),
        dunning_repository=repositories["dunning"],
        payment_repository=repositories["payment"],
        billing_repository=repositories["billing"],
        subscription_repository=repositories["subscription"],
        provider_registry=registry,
        policy=DunningPolicy(
            retry_intervals=(
                timedelta(days=1),
                timedelta(days=2),
                timedelta(days=3),
            ),
            grace_period=timedelta(days=7),
        ),
    )


@pytest.mark.asyncio
async def test_start_creates_retrying_dunning(
    payment,
    billing_record,
    repositories,
    provider_registry,
    now,
):
    repositories["dunning"].get_by_billing_record.return_value = None
    repositories["billing"].get_by_id.return_value = billing_record

    service = build_service(repositories, provider_registry)

    result = await service.start(
        payment=payment,
        now=now,
    )

    assert result.status == DunningStatus.RETRYING
    assert result.retry_count == 0
    assert result.next_retry_at == now + timedelta(days=1)
    assert result.grace_period_ends_at is None

    assert billing_record.status == BillingStatus.FAILED
    repositories["dunning"].add.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_is_idempotent_for_existing_dunning(
    payment,
    repositories,
    provider_registry,
    now,
):
    existing = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.RETRYING,
        retry_count=1,
        next_retry_at=now + timedelta(days=1),
    )

    repositories["dunning"].get_by_billing_record.return_value = existing

    service = build_service(repositories, provider_registry)

    result = await service.start(
        payment=payment,
        now=now,
    )

    assert result is existing
    repositories["dunning"].add.assert_not_awaited()


@pytest.mark.asyncio
async def test_retry_before_due_returns_none(
    payment,
    billing_record,
    subscription,
    repositories,
    provider_registry,
    now,
):
    dunning = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.RETRYING,
        retry_count=0,
        next_retry_at=now + timedelta(hours=1),
    )

    repositories["subscription"].get_by_id.return_value = subscription
    repositories["billing"].get_by_id.return_value = billing_record

    service = build_service(repositories, provider_registry)

    result = await service.retry(
        dunning=dunning,
        now=now,
    )

    assert result is None
    repositories["payment"].create.assert_not_awaited()


@pytest.mark.asyncio
async def test_retry_creates_new_pending_payment(
    payment,
    billing_record,
    subscription,
    repositories,
    provider_registry,
    now,
):
    dunning = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.RETRYING,
        retry_count=0,
        next_retry_at=now,
    )

    repositories["subscription"].get_by_id.return_value = subscription
    repositories["billing"].get_by_id.side_effect = [
        billing_record,
    ]
    repositories["payment"].get_all_by_billing_record.return_value = [
        payment,
    ]

    async def create(new_payment):
        return new_payment

    repositories["payment"].create.side_effect = create

    service = build_service(repositories, provider_registry)

    result = await service.retry(
        dunning=dunning,
        now=now,
    )

    assert result is not None
    assert result.id != payment.id
    assert result.status == PaymentStatus.PENDING
    assert result.billing_record_id == payment.billing_record_id
    assert result.subscription_id == payment.subscription_id
    assert result.provider == payment.provider
    assert result.amount == billing_record.amount
    assert result.currency == billing_record.currency

    _, provider = provider_registry
    provider.create_payment.assert_awaited_once_with(
        amount=result.amount,
        currency=result.currency,
        payment_id=str(result.id),
    )

    assert result.provider_payment_id == "retry-payment"
    assert dunning.retry_count == 1
    assert dunning.next_retry_at == now + timedelta(days=2)


@pytest.mark.asyncio
async def test_retry_after_final_attempt_enters_grace_period(
    payment,
    billing_record,
    subscription,
    repositories,
    provider_registry,
    now,
):
    dunning = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.RETRYING,
        retry_count=2,
        next_retry_at=now,
    )

    repositories["subscription"].get_by_id.return_value = subscription
    repositories["billing"].get_by_id.return_value = billing_record
    repositories["payment"].get_all_by_billing_record.return_value = [
        payment,
    ]

    async def create(new_payment):
        return new_payment

    repositories["payment"].create.side_effect = create

    service = build_service(repositories, provider_registry)

    result = await service.retry(
        dunning=dunning,
        now=now,
    )

    assert result is not None
    assert dunning.retry_count == 3
    assert dunning.status == DunningStatus.GRACE_PERIOD
    assert dunning.next_retry_at is None
    assert dunning.grace_period_ends_at == now + timedelta(days=7)


@pytest.mark.asyncio
async def test_recover_marks_dunning_recovered_and_billing_paid(
    payment,
    billing_record,
    repositories,
    provider_registry,
):
    dunning = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.RETRYING,
        retry_count=1,
        next_retry_at=datetime.now(timezone.utc),
    )

    repositories["dunning"].get_by_billing_record.return_value = dunning
    repositories["billing"].get_by_id.return_value = billing_record

    service = build_service(repositories, provider_registry)

    result = await service.recover(payment=payment)

    assert result is dunning
    assert dunning.status == DunningStatus.RECOVERED
    assert dunning.next_retry_at is None
    assert dunning.grace_period_ends_at is None
    assert billing_record.status == BillingStatus.PAID


@pytest.mark.asyncio
async def test_recover_reactivates_suspended_subscription(
    payment,
    billing_record,
    subscription,
    repositories,
    provider_registry,
):
    subscription.status = SubscriptionStatus.SUSPENDED

    dunning = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.SUSPENDED,
        retry_count=3,
    )

    repositories["dunning"].get_by_billing_record.return_value = dunning
    repositories["billing"].get_by_id.return_value = billing_record
    repositories["subscription"].get_by_id.return_value = subscription

    service = build_service(repositories, provider_registry)

    result = await service.recover(payment=payment)

    assert result is dunning
    assert dunning.status == DunningStatus.RECOVERED
    assert subscription.status == SubscriptionStatus.ACTIVE


@pytest.mark.asyncio
async def test_suspend_before_grace_expiry_is_noop(
    payment,
    subscription,
    repositories,
    provider_registry,
    now,
):
    dunning = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.GRACE_PERIOD,
        retry_count=3,
        grace_period_ends_at=now + timedelta(hours=1),
    )

    repositories["subscription"].get_by_id.return_value = subscription

    service = build_service(repositories, provider_registry)

    result = await service.suspend(
        dunning=dunning,
        now=now,
    )

    assert result is dunning
    assert dunning.status == DunningStatus.GRACE_PERIOD
    assert subscription.status == SubscriptionStatus.ACTIVE


@pytest.mark.asyncio
async def test_suspend_after_grace_expiry_suspends_subscription(
    payment,
    subscription,
    repositories,
    provider_registry,
    now,
):
    dunning = DunningRecord(
        id=uuid4(),
        organisation_id=payment.organisation_id,
        subscription_id=payment.subscription_id,
        billing_record_id=payment.billing_record_id,
        status=DunningStatus.GRACE_PERIOD,
        retry_count=3,
        grace_period_ends_at=now - timedelta(seconds=1),
    )

    repositories["subscription"].get_by_id.return_value = subscription

    service = build_service(repositories, provider_registry)

    result = await service.suspend(
        dunning=dunning,
        now=now,
    )

    assert result is dunning
    assert dunning.status == DunningStatus.SUSPENDED
    assert dunning.next_retry_at is None
    assert subscription.status == SubscriptionStatus.SUSPENDED
