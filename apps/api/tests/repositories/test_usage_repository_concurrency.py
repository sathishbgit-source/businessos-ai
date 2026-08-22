import asyncio
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.db.enums.plan import BillingInterval, PlanStatus
from app.db.enums.subscription import SubscriptionStatus
from app.db.enums.usage import UsageResource
from app.db.models.organisation import Organisation
from app.db.models.plan import Plan
from app.db.models.subscription import Subscription
from app.db.session import AsyncSessionLocal
from app.repositories.usage_repository import UsageRepository


@pytest.mark.asyncio
async def test_concurrent_consumption_cannot_exceed_limit():
    organisation_id = uuid4()
    subscription_id = uuid4()
    plan_id = uuid4()

    period_start = datetime(2026, 8, 1, tzinfo=timezone.utc)
    period_end = datetime(2026, 9, 1, tzinfo=timezone.utc)

    async with AsyncSessionLocal() as session:
        plan = Plan(
            id=plan_id,
            code=f"TEST-{uuid4().hex[:8]}",
            name="Concurrency Test Plan",
            description="Test plan for usage concurrency.",
            price=0,
            currency="USD",
            billing_interval=BillingInterval.MONTHLY,
            features=[],
            limits={"api_calls": 1},
            status=PlanStatus.ACTIVE,
        )

        organisation = Organisation(
            id=organisation_id,
            name="Usage Concurrency Test",
            slug=f"usage-concurrency-{uuid4().hex[:8]}",
        )

        subscription = Subscription(
            id=subscription_id,
            organisation_id=organisation_id,
            customer_id=uuid4(),
            plan_id=plan_id,
            status=SubscriptionStatus.ACTIVE,
            start_date=period_start,
            current_period_start=period_start,
            current_period_end=period_end,
        )

        session.add_all([plan, organisation, subscription])
        await session.commit()

    async def consume():
        async with AsyncSessionLocal() as session:
            repository = UsageRepository(session)

            result = await repository.consume_if_within_limit(
                organisation_id=organisation_id,
                subscription_id=subscription_id,
                resource=UsageResource.API_CALLS,
                period_start=period_start,
                period_end=period_end,
                limit=1,
                quantity=1,
            )

            await session.commit()

            return result is not None

    results = await asyncio.gather(
        consume(),
        consume(),
    )

    assert sorted(results) == [False, True]

    async with AsyncSessionLocal() as session:
        repository = UsageRepository(session)

        record = await repository.get(
            organisation_id=organisation_id,
            subscription_id=subscription_id,
            resource=UsageResource.API_CALLS,
            period_start=period_start,
            period_end=period_end,
        )

        assert record is not None
        assert record.used == 1

        await session.delete(subscription)
        await session.delete(organisation)
        await session.delete(plan)
        await session.commit()
