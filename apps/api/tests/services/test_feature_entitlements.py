from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.core.exceptions import FeatureNotEntitled
from app.db.enums.entitlement import Feature
from app.db.enums.subscription import SubscriptionStatus
from app.services.entitlement.check_feature_access import (
    FeatureEntitlementService,
)


def make_service():
    subscription_repository = Mock()
    plan_repository = Mock()

    service = FeatureEntitlementService(
        subscription_repository=subscription_repository,
        plan_repository=plan_repository,
    )

    return service, subscription_repository, plan_repository


def make_subscription(
    *,
    plan_id=None,
    status=SubscriptionStatus.ACTIVE,
):
    subscription = Mock()
    subscription.plan_id = plan_id or uuid4()
    subscription.status = status
    return subscription


def make_plan(*features):
    plan = Mock()
    plan.features = list(features)
    return plan


@pytest.mark.asyncio
async def test_has_feature_returns_true_when_feature_is_entitled():
    service, subscription_repository, plan_repository = make_service()

    organisation_id = uuid4()
    plan_id = uuid4()

    subscription_repository.get_active_by_organisation = AsyncMock(
        return_value=make_subscription(plan_id=plan_id)
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=make_plan(Feature.AUTOMATION.value)
    )

    result = await service.has_feature(
        organisation_id=organisation_id,
        feature=Feature.AUTOMATION,
    )

    assert result is True
    subscription_repository.get_active_by_organisation.assert_awaited_once_with(
        organisation_id=organisation_id,
    )
    plan_repository.get_by_id.assert_awaited_once_with(plan_id)


@pytest.mark.asyncio
async def test_has_feature_returns_false_when_feature_is_not_entitled():
    service, subscription_repository, plan_repository = make_service()

    plan_id = uuid4()

    subscription_repository.get_active_by_organisation = AsyncMock(
        return_value=make_subscription(plan_id=plan_id)
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=make_plan(Feature.BASIC_REPORTS.value)
    )

    result = await service.has_feature(
        organisation_id=uuid4(),
        feature=Feature.AUTOMATION,
    )

    assert result is False


@pytest.mark.asyncio
async def test_has_feature_returns_false_without_active_subscription():
    service, subscription_repository, plan_repository = make_service()

    subscription_repository.get_active_by_organisation = AsyncMock(
        return_value=None
    )

    result = await service.has_feature(
        organisation_id=uuid4(),
        feature=Feature.AUTOMATION,
    )

    assert result is False
    plan_repository.get_by_id.assert_not_called()


@pytest.mark.asyncio
async def test_has_feature_returns_false_when_plan_is_missing():
    service, subscription_repository, plan_repository = make_service()

    plan_id = uuid4()

    subscription_repository.get_active_by_organisation = AsyncMock(
        return_value=make_subscription(plan_id=plan_id)
    )
    plan_repository.get_by_id = AsyncMock(return_value=None)

    result = await service.has_feature(
        organisation_id=uuid4(),
        feature=Feature.AUTOMATION,
    )

    assert result is False


@pytest.mark.asyncio
async def test_require_feature_succeeds_when_entitled():
    service, subscription_repository, plan_repository = make_service()

    plan_id = uuid4()

    subscription_repository.get_active_by_organisation = AsyncMock(
        return_value=make_subscription(plan_id=plan_id)
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=make_plan(Feature.AUTOMATION.value)
    )

    result = await service.require_feature(
        organisation_id=uuid4(),
        feature=Feature.AUTOMATION,
    )

    assert result is None


@pytest.mark.asyncio
async def test_require_feature_raises_when_not_entitled():
    service, subscription_repository, plan_repository = make_service()

    plan_id = uuid4()

    subscription_repository.get_active_by_organisation = AsyncMock(
        return_value=make_subscription(plan_id=plan_id)
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=make_plan(Feature.BASIC_REPORTS.value)
    )

    with pytest.raises(FeatureNotEntitled):
        await service.require_feature(
            organisation_id=uuid4(),
            feature=Feature.AUTOMATION,
        )
