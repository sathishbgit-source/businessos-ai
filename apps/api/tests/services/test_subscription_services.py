from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    InvalidSubscriptionPeriod,
    OrganisationAccessDenied,
    PlanInactive,
    PlanNotFound,
    SubscriptionAccessDenied,
    SubscriptionNotFound,
    SubscriptionStateTransitionDenied,
)
from app.db.enums import MemberStatus, PlanStatus, SubscriptionStatus
from app.db.models.subscription import Subscription
from app.services.subscription.create_subscription import (
    CreateSubscriptionService,
)
from app.services.subscription.update_subscription import (
    UpdateSubscriptionService,
)


def make_datetime(day: int) -> datetime:
    return datetime(
        2026,
        8,
        day,
        tzinfo=timezone.utc,
    )


def make_member(status=MemberStatus.ACTIVE):
    member = Mock()
    member.status = status
    return member


def make_plan(status=PlanStatus.ACTIVE):
    plan = Mock()
    plan.id = uuid4()
    plan.code = "STARTER"
    plan.price = Decimal("79.00")
    plan.currency = "AUD"
    plan.status = status
    return plan


def make_subscription(
    *,
    organisation_id=None,
    status=SubscriptionStatus.ACTIVE,
):
    organisation_id = organisation_id or uuid4()

    subscription = Mock(spec=Subscription)
    subscription.id = uuid4()
    subscription.organisation_id = organisation_id
    subscription.customer_id = uuid4()
    subscription.plan_id = uuid4()
    subscription.status = status
    subscription.start_date = make_datetime(1)
    subscription.current_period_start = make_datetime(1)
    subscription.current_period_end = make_datetime(31)

    return subscription


def make_create_service():
    db = AsyncMock()
    subscription_repository = Mock()
    organisation_member_repository = Mock()
    plan_repository = Mock()

    service = CreateSubscriptionService(
        db=db,
        subscription_repository=subscription_repository,
        organisation_member_repository=organisation_member_repository,
        plan_repository=plan_repository,
    )

    return (
        service,
        db,
        subscription_repository,
        organisation_member_repository,
        plan_repository,
    )


def make_update_service():
    db = AsyncMock()
    subscription_repository = Mock()
    organisation_member_repository = Mock()

    service = UpdateSubscriptionService(
        db=db,
        subscription_repository=subscription_repository,
        organisation_member_repository=organisation_member_repository,
    )

    return (
        service,
        db,
        subscription_repository,
        organisation_member_repository,
    )


@pytest.mark.asyncio
async def test_create_subscription_success():
    (
        service,
        db,
        subscription_repository,
        organisation_member_repository,
        plan_repository,
    ) = make_create_service()

    organisation_id = uuid4()
    user_id = uuid4()
    plan = make_plan()

    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )
    plan_repository.get_by_id = AsyncMock(return_value=plan)

    created = make_subscription(organisation_id=organisation_id)
    subscription_repository.create = AsyncMock(return_value=created)

    result = await service.execute(
        organisation_id=organisation_id,
        user_id=user_id,
        customer_id=uuid4(),
        plan_id=plan.id,
        start_date=make_datetime(1),
        current_period_start=make_datetime(1),
        current_period_end=make_datetime(31),
    )

    assert result is created
    subscription_repository.create.assert_awaited_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(created)


@pytest.mark.asyncio
async def test_create_subscription_rejects_missing_plan():
    (
        service,
        _,
        _,
        organisation_member_repository,
        plan_repository,
    ) = make_create_service()

    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )
    plan_repository.get_by_id = AsyncMock(return_value=None)

    plan_id = uuid4()

    with pytest.raises(PlanNotFound):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            customer_id=uuid4(),
            plan_id=plan_id,
            start_date=make_datetime(1),
            current_period_start=make_datetime(1),
            current_period_end=make_datetime(31),
        )


@pytest.mark.asyncio
async def test_create_subscription_rejects_inactive_plan():
    (
        service,
        _,
        _,
        organisation_member_repository,
        plan_repository,
    ) = make_create_service()

    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )

    plan = make_plan(status=PlanStatus.DISABLED)
    plan_repository.get_by_id = AsyncMock(return_value=plan)

    with pytest.raises(PlanInactive):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            customer_id=uuid4(),
            plan_id=plan.id,
            start_date=make_datetime(1),
            current_period_start=make_datetime(1),
            current_period_end=make_datetime(31),
        )


@pytest.mark.asyncio
async def test_create_subscription_rejects_invalid_period():
    (
        service,
        _,
        _,
        organisation_member_repository,
        plan_repository,
    ) = make_create_service()

    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )

    plan = make_plan()
    plan_repository.get_by_id = AsyncMock(return_value=plan)

    with pytest.raises(InvalidSubscriptionPeriod):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            customer_id=uuid4(),
            plan_id=plan.id,
            start_date=make_datetime(1),
            current_period_start=make_datetime(31),
            current_period_end=make_datetime(1),
        )


@pytest.mark.asyncio
async def test_create_subscription_rejects_period_before_start_date():
    (
        service,
        _,
        _,
        organisation_member_repository,
        plan_repository,
    ) = make_create_service()

    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )

    plan = make_plan()
    plan_repository.get_by_id = AsyncMock(return_value=plan)

    with pytest.raises(InvalidSubscriptionPeriod):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            customer_id=uuid4(),
            plan_id=plan.id,
            start_date=make_datetime(15),
            current_period_start=make_datetime(1),
            current_period_end=make_datetime(31),
        )


@pytest.mark.asyncio
async def test_create_subscription_rejects_inactive_member():
    (
        service,
        _,
        _,
        organisation_member_repository,
        _,
    ) = make_create_service()

    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member(status=MemberStatus.INACTIVE))
    )

    with pytest.raises(OrganisationAccessDenied):
        await service.execute(
            organisation_id=uuid4(),
            user_id=uuid4(),
            customer_id=uuid4(),
            plan_id=uuid4(),
            start_date=make_datetime(1),
            current_period_start=make_datetime(1),
            current_period_end=make_datetime(31),
        )


@pytest.mark.asyncio
async def test_update_subscription_success():
    (
        service,
        db,
        subscription_repository,
        organisation_member_repository,
    ) = make_update_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id,
        status=SubscriptionStatus.ACTIVE,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    subscription_repository.update = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )

    result = await service.execute(
        subscription_id=subscription.id,
        organisation_id=organisation_id,
        user_id=uuid4(),
        status=SubscriptionStatus.CANCELLED,
    )

    assert result is subscription
    assert subscription.status == SubscriptionStatus.CANCELLED
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_subscription_rejects_cancelled_to_active():
    (
        service,
        _,
        subscription_repository,
        organisation_member_repository,
    ) = make_update_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id,
        status=SubscriptionStatus.CANCELLED,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )

    with pytest.raises(SubscriptionStateTransitionDenied):
        await service.execute(
            subscription_id=subscription.id,
            organisation_id=organisation_id,
            user_id=uuid4(),
            status=SubscriptionStatus.ACTIVE,
        )


@pytest.mark.asyncio
async def test_update_subscription_rejects_invalid_period():
    (
        service,
        _,
        subscription_repository,
        organisation_member_repository,
    ) = make_update_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id,
        status=SubscriptionStatus.ACTIVE,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )

    with pytest.raises(InvalidSubscriptionPeriod):
        await service.execute(
            subscription_id=subscription.id,
            organisation_id=organisation_id,
            user_id=uuid4(),
            current_period_start=make_datetime(31),
            current_period_end=make_datetime(15),
        )


@pytest.mark.asyncio
async def test_update_subscription_rejects_period_before_start_date():
    (
        service,
        _,
        subscription_repository,
        organisation_member_repository,
    ) = make_update_service()

    organisation_id = uuid4()
    subscription = make_subscription(
        organisation_id=organisation_id,
        status=SubscriptionStatus.ACTIVE,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )
    organisation_member_repository.get_by_organisation_and_user = (
        AsyncMock(return_value=make_member())
    )

    with pytest.raises(InvalidSubscriptionPeriod):
        await service.execute(
            subscription_id=subscription.id,
            organisation_id=organisation_id,
            user_id=uuid4(),
            current_period_start=datetime(2026, 7, 31, tzinfo=timezone.utc),
            current_period_end=make_datetime(15),
        )


@pytest.mark.asyncio
async def test_update_subscription_rejects_missing_subscription():
    (
        service,
        _,
        subscription_repository,
        _,
    ) = make_update_service()

    subscription_repository.get_by_id = AsyncMock(return_value=None)

    with pytest.raises(SubscriptionNotFound):
        await service.execute(
            subscription_id=uuid4(),
            organisation_id=uuid4(),
            user_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_update_subscription_rejects_other_organisation():
    (
        service,
        _,
        subscription_repository,
        _,
    ) = make_update_service()

    requested_organisation_id = uuid4()
    actual_organisation_id = uuid4()

    subscription = make_subscription(
        organisation_id=actual_organisation_id,
    )

    subscription_repository.get_by_id = AsyncMock(
        return_value=subscription
    )

    with pytest.raises(SubscriptionAccessDenied):
        await service.execute(
            subscription_id=subscription.id,
            organisation_id=requested_organisation_id,
            user_id=uuid4(),
        )
