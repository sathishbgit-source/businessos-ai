from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    UsageLimitConfigurationError,
    UsageLimitExceeded,
)
from app.db.enums.usage import UsageResource
from app.services.usage.usage_limit_service import UsageLimitService


PERIOD_START = datetime(2026, 8, 1, tzinfo=timezone.utc)
PERIOD_END = datetime(2026, 9, 1, tzinfo=timezone.utc)


def make_subscription():
    subscription = Mock()
    subscription.id = uuid4()
    subscription.plan_id = uuid4()
    subscription.current_period_start = PERIOD_START
    subscription.current_period_end = PERIOD_END
    return subscription


def make_plan(limits=None):
    plan = Mock()
    plan.id = uuid4()
    plan.limits = limits if limits is not None else {"api_calls": 100}
    return plan


def make_record(used=0):
    record = Mock()
    record.used = used
    return record


def make_service():
    subscription_repository = Mock()
    plan_repository = Mock()
    usage_repository = Mock()
    usage_repository.get = AsyncMock()
    usage_repository.consume_if_within_limit = AsyncMock()

    service = UsageLimitService(
        subscription_repository=subscription_repository,
        plan_repository=plan_repository,
        usage_repository=usage_repository,
    )

    return (
        service,
        subscription_repository,
        plan_repository,
        usage_repository,
    )


@pytest.mark.asyncio
async def test_get_limit_returns_configured_plan_limit():
    service, subscription_repo, plan_repo, _ = make_service()

    subscription = make_subscription()
    plan = make_plan({"api_calls": 100})

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=subscription,
    )
    plan_repo.get_by_id = AsyncMock(
        return_value=plan,
    )

    result = await service.get_limit(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
    )

    assert result == 100


@pytest.mark.asyncio
async def test_get_limit_returns_none_without_subscription():
    service, subscription_repo, _, _ = make_service()

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=None,
    )

    result = await service.get_limit(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
    )

    assert result is None


@pytest.mark.asyncio
async def test_missing_resource_limit_raises_configuration_error():
    service, subscription_repo, plan_repo, _ = make_service()

    subscription = make_subscription()
    plan = make_plan({"users": 10})

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=subscription,
    )
    plan_repo.get_by_id = AsyncMock(
        return_value=plan,
    )

    with pytest.raises(UsageLimitConfigurationError):
        await service.get_limit(
            organisation_id=uuid4(),
            resource=UsageResource.API_CALLS,
        )


@pytest.mark.asyncio
async def test_get_usage_returns_zero_without_subscription():
    service, subscription_repo, _, usage_repo = make_service()

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=None,
    )
    usage_repo.get = AsyncMock()

    result = await service.get_usage(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
    )

    assert result == 0
    usage_repo.get.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_usage_returns_persisted_current_period_usage():
    service, subscription_repo, _, usage_repo = make_service()

    subscription = make_subscription()
    record = make_record(37)

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=subscription,
    )
    usage_repo.get = AsyncMock(
        return_value=record,
    )

    result = await service.get_usage(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
    )

    assert result == 37

    usage_repo.get.assert_awaited_once_with(
        organisation_id=subscription_repo
        .get_active_by_organisation.await_args.kwargs["organisation_id"],
        subscription_id=subscription.id,
        resource=UsageResource.API_CALLS,
        period_start=PERIOD_START,
        period_end=PERIOD_END,
    )


@pytest.mark.asyncio
async def test_check_limit_allows_exact_boundary():
    service, subscription_repo, plan_repo, usage_repo = make_service()

    subscription = make_subscription()
    plan = make_plan({"api_calls": 100})
    record = make_record(99)

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=subscription,
    )
    plan_repo.get_by_id = AsyncMock(
        return_value=plan,
    )
    usage_repo.get = AsyncMock(
        return_value=record,
    )

    result = await service.check_limit(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
        quantity=1,
    )

    assert result is True


@pytest.mark.asyncio
async def test_check_limit_rejects_exceeding_usage():
    service, subscription_repo, plan_repo, usage_repo = make_service()

    subscription = make_subscription()
    plan = make_plan({"api_calls": 100})
    record = make_record(100)

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=subscription,
    )
    plan_repo.get_by_id = AsyncMock(
        return_value=plan,
    )
    usage_repo.get = AsyncMock(
        return_value=record,
    )

    result = await service.check_limit(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
        quantity=1,
    )

    assert result is False


@pytest.mark.asyncio
async def test_check_limit_denies_without_subscription():
    service, subscription_repo, _, _ = make_service()

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=None,
    )

    result = await service.check_limit(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
    )

    assert result is False


@pytest.mark.asyncio
async def test_consume_returns_record_on_success():
    service, subscription_repo, plan_repo, usage_repo = make_service()

    subscription = make_subscription()
    plan = make_plan({"api_calls": 100})
    record = make_record(10)
    consumed = make_record(11)

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=subscription,
    )
    plan_repo.get_by_id = AsyncMock(
        return_value=plan,
    )
    usage_repo.get = AsyncMock(
        return_value=record,
    )
    usage_repo.consume_if_within_limit = AsyncMock(
        return_value=consumed,
    )

    result = await service.consume(
        organisation_id=uuid4(),
        resource=UsageResource.API_CALLS,
        quantity=1,
    )

    assert result is consumed

    usage_repo.consume_if_within_limit.assert_awaited_once_with(
        organisation_id=subscription_repo
        .get_active_by_organisation.await_args.kwargs["organisation_id"],
        subscription_id=subscription.id,
        resource=UsageResource.API_CALLS,
        period_start=PERIOD_START,
        period_end=PERIOD_END,
        limit=100,
        quantity=1,
    )


@pytest.mark.asyncio
async def test_consume_raises_when_atomic_repository_rejects():
    service, subscription_repo, plan_repo, usage_repo = make_service()

    subscription = make_subscription()
    plan = make_plan({"api_calls": 100})
    record = make_record(100)

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=subscription,
    )
    plan_repo.get_by_id = AsyncMock(
        return_value=plan,
    )
    usage_repo.get = AsyncMock(
        return_value=record,
    )
    usage_repo.consume_if_within_limit = AsyncMock(
        return_value=None,
    )

    organisation_id = uuid4()

    with pytest.raises(UsageLimitExceeded) as exc_info:
        await service.consume(
            organisation_id=organisation_id,
            resource=UsageResource.API_CALLS,
            quantity=1,
        )

    error = exc_info.value

    assert error.resource == "api_calls"
    assert error.limit == 100
    assert error.current_usage == 100
    assert error.requested_quantity == 1


@pytest.mark.asyncio
async def test_consume_denies_without_subscription():
    service, subscription_repo, _, usage_repo = make_service()

    subscription_repo.get_active_by_organisation = AsyncMock(
        return_value=None,
    )

    with pytest.raises(UsageLimitExceeded) as exc_info:
        await service.consume(
            organisation_id=uuid4(),
            resource=UsageResource.API_CALLS,
        )

    error = exc_info.value

    assert error.resource == "api_calls"
    assert error.limit == 0
    assert error.current_usage == 0
    assert error.requested_quantity == 1

    usage_repo.consume_if_within_limit.assert_not_awaited()


@pytest.mark.asyncio
async def test_zero_quantity_is_rejected():
    service, _, _, _ = make_service()

    with pytest.raises(
        ValueError,
        match="quantity must be greater than zero",
    ):
        await service.check_limit(
            organisation_id=uuid4(),
            resource=UsageResource.API_CALLS,
            quantity=0,
        )


@pytest.mark.asyncio
async def test_negative_quantity_is_rejected():
    service, _, _, _ = make_service()

    with pytest.raises(
        ValueError,
        match="quantity must be greater than zero",
    ):
        await service.consume(
            organisation_id=uuid4(),
            resource=UsageResource.API_CALLS,
            quantity=-1,
        )
