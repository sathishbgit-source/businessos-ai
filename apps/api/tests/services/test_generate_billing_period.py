from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    OrganisationAccessDenied,
    PlanInactive,
    PlanNotFound,
    SubscriptionNotFound,
)
from app.db.enums import BillingInterval, PlanStatus
from app.db.models.subscription import Subscription
from app.services.billing.generate_billing_period import (
    GenerateBillingPeriodService,
)


def make_subscription(
    *,
    organisation_id=None,
):
    organisation_id = organisation_id or uuid4()

    subscription = Mock(spec=Subscription)
    subscription.id = uuid4()
    subscription.organisation_id = organisation_id
    subscription.customer_id = uuid4()
    subscription.plan_id = uuid4()
    subscription.current_period_start = datetime(
        2026,
        1,
        15,
        tzinfo=timezone.utc,
    )
    subscription.current_period_end = datetime(
        2026,
        2,
        15,
        tzinfo=timezone.utc,
    )

    return subscription


def make_plan(
    *,
    billing_interval=BillingInterval.MONTHLY,
    status=PlanStatus.ACTIVE,
):
    plan = Mock()
    plan.id = uuid4()
    plan.code = "STARTER"
    plan.price = Decimal("79.00")
    plan.currency = "AUD"
    plan.billing_interval = billing_interval
    plan.status = status

    return plan


def make_service():
    db = AsyncMock()
    billing_repository = Mock()
    organisation_member_repository = Mock()
    subscription_repository = Mock()
    plan_repository = Mock()

    service = GenerateBillingPeriodService(
        db=db,
        billing_repository=billing_repository,
        organisation_member_repository=organisation_member_repository,
        subscription_repository=subscription_repository,
        plan_repository=plan_repository,
    )

    return (
        service,
        subscription_repository,
        plan_repository,
    )


@pytest.mark.asyncio
async def test_generates_next_monthly_billing_period():
    (
        service,
        subscription_repository,
        plan_repository,
    ) = make_service()

    organisation_id = uuid4()
    user_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id,
    )
    plan = make_plan(
        billing_interval=BillingInterval.MONTHLY,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription,
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=plan,
    )

    billing_record = Mock()
    service.create_billing_record_service.execute = AsyncMock(
        return_value=billing_record,
    )

    result = await service.execute(
        organisation_id=organisation_id,
        user_id=user_id,
        subscription_id=subscription.id,
    )

    assert result is billing_record

    service.create_billing_record_service.execute.assert_awaited_once_with(
        organisation_id=organisation_id,
        user_id=user_id,
        subscription_id=subscription.id,
        billing_period_start=datetime(
            2026,
            2,
            15,
            tzinfo=timezone.utc,
        ),
        billing_period_end=datetime(
            2026,
            3,
            15,
            tzinfo=timezone.utc,
        ),
    )


@pytest.mark.asyncio
async def test_generates_next_yearly_billing_period():
    (
        service,
        subscription_repository,
        plan_repository,
    ) = make_service()

    organisation_id = uuid4()
    user_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id,
    )
    subscription.current_period_start = datetime(
        2026,
        1,
        15,
        tzinfo=timezone.utc,
    )
    subscription.current_period_end = datetime(
        2027,
        1,
        15,
        tzinfo=timezone.utc,
    )

    plan = make_plan(
        billing_interval=BillingInterval.YEARLY,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription,
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=plan,
    )

    billing_record = Mock()
    service.create_billing_record_service.execute = AsyncMock(
        return_value=billing_record,
    )

    result = await service.execute(
        organisation_id=organisation_id,
        user_id=user_id,
        subscription_id=subscription.id,
    )

    assert result is billing_record

    service.create_billing_record_service.execute.assert_awaited_once_with(
        organisation_id=organisation_id,
        user_id=user_id,
        subscription_id=subscription.id,
        billing_period_start=datetime(
            2027,
            1,
            15,
            tzinfo=timezone.utc,
        ),
        billing_period_end=datetime(
            2028,
            1,
            15,
            tzinfo=timezone.utc,
        ),
    )


@pytest.mark.asyncio
async def test_rejects_missing_subscription():
    (
        service,
        subscription_repository,
        _,
    ) = make_service()

    subscription_repository.get_by_id = AsyncMock(
        return_value=None,
    )

    with pytest.raises(SubscriptionNotFound):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            subscription_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_rejects_subscription_from_another_organisation():
    (
        service,
        subscription_repository,
        _,
    ) = make_service()

    subscription = make_subscription()
    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription,
    )

    with pytest.raises(OrganisationAccessDenied):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            subscription_id=subscription.id,
        )


@pytest.mark.asyncio
async def test_rejects_missing_plan():
    (
        service,
        subscription_repository,
        plan_repository,
    ) = make_service()

    subscription = make_subscription()
    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription,
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=None,
    )

    with pytest.raises(PlanNotFound):
        await service.execute(
            organisation_id=subscription.organisation_id,
            user_id=uuid4(),
            subscription_id=subscription.id,
        )


@pytest.mark.asyncio
async def test_rejects_inactive_plan():
    (
        service,
        subscription_repository,
        plan_repository,
    ) = make_service()

    subscription = make_subscription()
    plan = make_plan(
        status=PlanStatus.DISABLED,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription,
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=plan,
    )

    with pytest.raises(PlanInactive):
        await service.execute(
            organisation_id=subscription.organisation_id,
            user_id=uuid4(),
            subscription_id=subscription.id,
        )
