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
    SubscriptionStateTransitionDenied,
)
from app.db.enums import BillingInterval, MemberStatus, PlanStatus, SubscriptionStatus
from app.db.models.subscription import Subscription
from app.services.subscription.renew_subscription import (
    RenewSubscriptionService,
)


def make_subscription(*, organisation_id=None):
    organisation_id = organisation_id or uuid4()

    subscription = Mock(spec=Subscription)
    subscription.id = uuid4()
    subscription.organisation_id = organisation_id
    subscription.customer_id = uuid4()
    subscription.plan_id = uuid4()
    subscription.status = SubscriptionStatus.ACTIVE
    subscription.start_date = datetime(
        2026, 1, 15, tzinfo=timezone.utc
    )
    subscription.current_period_start = datetime(
        2026, 1, 15, tzinfo=timezone.utc
    )
    subscription.current_period_end = datetime(
        2026, 2, 15, tzinfo=timezone.utc
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
    plan_repository = Mock()
    subscription_repository = Mock()

    service = RenewSubscriptionService(
        db=db,
        billing_repository=billing_repository,
        organisation_member_repository=organisation_member_repository,
        plan_repository=plan_repository,
        subscription_repository=subscription_repository,
    )

    return (
        service,
        db,
        billing_repository,
        organisation_member_repository,
        plan_repository,
        subscription_repository,
    )


def configure_successful_renewal(
    *,
    subscription,
    plan,
    organisation_member_repository,
    plan_repository,
    subscription_repository,
    billing_repository,
):
    member = Mock()
    member.status = MemberStatus.ACTIVE

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=member)
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=plan
    )
    billing_repository.create = AsyncMock()
    subscription_repository.update = AsyncMock(
        side_effect=lambda value: value
    )


@pytest.mark.asyncio
async def test_renews_monthly_subscription():
    (
        service,
        db,
        billing_repository,
        organisation_member_repository,
        plan_repository,
        subscription_repository,
    ) = make_service()

    organisation_id = uuid4()
    user_id = uuid4()

    subscription = make_subscription(
        organisation_id=organisation_id
    )
    plan = make_plan()

    configure_successful_renewal(
        subscription=subscription,
        plan=plan,
        organisation_member_repository=organisation_member_repository,
        plan_repository=plan_repository,
        subscription_repository=subscription_repository,
        billing_repository=billing_repository,
    )

    result = await service.execute(
        organisation_id=organisation_id,
        user_id=user_id,
        subscription_id=subscription.id,
    )

    assert result is subscription

    assert subscription.current_period_start == datetime(
        2026, 2, 15, tzinfo=timezone.utc
    )
    assert subscription.current_period_end == datetime(
        2026, 3, 15, tzinfo=timezone.utc
    )

    billing_record = billing_repository.create.await_args.args[0]

    assert billing_record.subscription_id == subscription.id
    assert billing_record.customer_id == subscription.customer_id
    assert billing_record.plan_id == plan.id
    assert billing_record.billing_period_start == datetime(
        2026, 2, 15, tzinfo=timezone.utc
    )
    assert billing_record.billing_period_end == datetime(
        2026, 3, 15, tzinfo=timezone.utc
    )
    assert billing_record.amount == plan.price
    assert billing_record.currency == plan.currency

    subscription_repository.update.assert_awaited_once_with(
        subscription
    )
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(subscription)


@pytest.mark.asyncio
async def test_renews_yearly_subscription():
    (
        service,
        _,
        billing_repository,
        organisation_member_repository,
        plan_repository,
        subscription_repository,
    ) = make_service()

    organisation_id = uuid4()

    subscription = make_subscription(
        organisation_id=organisation_id
    )
    subscription.current_period_end = datetime(
        2027, 1, 15, tzinfo=timezone.utc
    )

    plan = make_plan(
        billing_interval=BillingInterval.YEARLY
    )

    configure_successful_renewal(
        subscription=subscription,
        plan=plan,
        organisation_member_repository=organisation_member_repository,
        plan_repository=plan_repository,
        subscription_repository=subscription_repository,
        billing_repository=billing_repository,
    )

    await service.execute(
        organisation_id=organisation_id,
        user_id=uuid4(),
        subscription_id=subscription.id,
    )

    billing_record = billing_repository.create.await_args.args[0]

    assert billing_record.billing_period_start == datetime(
        2027, 1, 15, tzinfo=timezone.utc
    )
    assert billing_record.billing_period_end == datetime(
        2028, 1, 15, tzinfo=timezone.utc
    )

    assert subscription.current_period_start == datetime(
        2027, 1, 15, tzinfo=timezone.utc
    )
    assert subscription.current_period_end == datetime(
        2028, 1, 15, tzinfo=timezone.utc
    )


@pytest.mark.asyncio
async def test_rejects_missing_subscription():
    (
        service,
        _,
        _,
        _,
        _,
        subscription_repository,
    ) = make_service()

    subscription_repository.get_by_id = AsyncMock(
        return_value=None
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
        _,
        _,
        _,
        _,
        subscription_repository,
    ) = make_service()

    subscription = make_subscription()

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )

    with pytest.raises(OrganisationAccessDenied):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            subscription_id=subscription.id,
        )


@pytest.mark.asyncio
async def test_rejects_unauthorised_member():
    (
        service,
        _,
        _,
        organisation_member_repository,
        _,
        subscription_repository,
    ) = make_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=None)
    )

    with pytest.raises(OrganisationAccessDenied):
        await service.execute(
            organisation_id=organisation_id,
            user_id=uuid4(),
            subscription_id=subscription.id,
        )


@pytest.mark.asyncio
async def test_rejects_inactive_subscription():
    (
        service,
        _,
        _,
        organisation_member_repository,
        _,
        subscription_repository,
    ) = make_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id
    )
    subscription.status = SubscriptionStatus.CANCELLED

    member = Mock()
    member.status = MemberStatus.ACTIVE

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=member)
    )

    with pytest.raises(SubscriptionStateTransitionDenied):
        await service.execute(
            organisation_id=organisation_id,
            user_id=uuid4(),
            subscription_id=subscription.id,
        )


@pytest.mark.asyncio
async def test_rejects_missing_plan():
    (
        service,
        _,
        _,
        organisation_member_repository,
        plan_repository,
        subscription_repository,
    ) = make_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id
    )

    member = Mock()
    member.status = MemberStatus.ACTIVE

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=member)
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=None
    )

    with pytest.raises(PlanNotFound):
        await service.execute(
            organisation_id=organisation_id,
            user_id=uuid4(),
            subscription_id=subscription.id,
        )


@pytest.mark.asyncio
async def test_rejects_inactive_plan():
    (
        service,
        _,
        _,
        organisation_member_repository,
        plan_repository,
        subscription_repository,
    ) = make_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id
    )
    plan = make_plan(
        status=PlanStatus.DISABLED
    )

    member = Mock()
    member.status = MemberStatus.ACTIVE

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=member)
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=plan
    )

    with pytest.raises(PlanInactive):
        await service.execute(
            organisation_id=organisation_id,
            user_id=uuid4(),
            subscription_id=subscription.id,
        )
