from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.db.enums.usage import UsageResource
from app.db.models.usage_record import UsageRecord
from app.repositories.usage_repository import UsageRepository


def make_result(*, scalar_one_or_none=None):
    result = Mock()
    result.scalar_one_or_none.return_value = scalar_one_or_none
    return result


def make_record(*, used=0):
    record = Mock(spec=UsageRecord)
    record.id = uuid4()
    record.used = used
    return record


@pytest.mark.asyncio
async def test_get_filters_by_usage_scope():
    session = AsyncMock()

    record = make_record(used=4)
    session.execute.return_value = make_result(
        scalar_one_or_none=record,
    )

    repository = UsageRepository(session)

    organisation_id = uuid4()
    subscription_id = uuid4()
    period_start = datetime(2026, 8, 1, tzinfo=timezone.utc)
    period_end = datetime(2026, 9, 1, tzinfo=timezone.utc)

    returned = await repository.get(
        organisation_id=organisation_id,
        subscription_id=subscription_id,
        resource=UsageResource.API_CALLS,
        period_start=period_start,
        period_end=period_end,
    )

    assert returned is record
    session.execute.assert_awaited_once()

    statement = session.execute.await_args.args[0]

    compiled = statement.compile(
        compile_kwargs={"literal_binds": True},
    )

    sql = str(compiled)

    assert "usage_records.organisation_id" in sql
    assert "usage_records.subscription_id" in sql
    assert "usage_records.resource" in sql
    assert "usage_records.period_start" in sql
    assert "usage_records.period_end" in sql


@pytest.mark.asyncio
async def test_get_returns_none_when_not_found():
    session = AsyncMock()

    session.execute.return_value = make_result(
        scalar_one_or_none=None,
    )

    repository = UsageRepository(session)

    returned = await repository.get(
        organisation_id=uuid4(),
        subscription_id=uuid4(),
        resource=UsageResource.USERS,
        period_start=datetime(2026, 8, 1, tzinfo=timezone.utc),
        period_end=datetime(2026, 9, 1, tzinfo=timezone.utc),
    )

    assert returned is None
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_or_create_inserts_zero_usage_when_missing():
    session = AsyncMock()

    record = make_record(used=0)

    session.execute.side_effect = [
        Mock(),
        make_result(scalar_one_or_none=record),
    ]

    repository = UsageRepository(session)

    returned = await repository.get_or_create(
        organisation_id=uuid4(),
        subscription_id=uuid4(),
        resource=UsageResource.RECORDS,
        period_start=datetime(2026, 8, 1, tzinfo=timezone.utc),
        period_end=datetime(2026, 9, 1, tzinfo=timezone.utc),
    )

    assert returned is record
    assert session.execute.await_count == 2
    session.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_consume_rejects_non_positive_quantity():
    session = AsyncMock()
    repository = UsageRepository(session)

    with pytest.raises(
        ValueError,
        match="quantity must be greater than zero",
    ):
        await repository.consume_if_within_limit(
            organisation_id=uuid4(),
            subscription_id=uuid4(),
            resource=UsageResource.MODULES,
            period_start=datetime(2026, 8, 1, tzinfo=timezone.utc),
            period_end=datetime(2026, 9, 1, tzinfo=timezone.utc),
            limit=10,
            quantity=0,
        )

    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_consume_returns_none_when_atomic_update_hits_limit():
    session = AsyncMock()

    record = make_record(used=9)

    session.execute.side_effect = [
        Mock(),
        make_result(scalar_one_or_none=record),
        make_result(scalar_one_or_none=None),
    ]

    repository = UsageRepository(session)

    returned = await repository.consume_if_within_limit(
        organisation_id=uuid4(),
        subscription_id=uuid4(),
        resource=UsageResource.TRANSACTIONS,
        period_start=datetime(2026, 8, 1, tzinfo=timezone.utc),
        period_end=datetime(2026, 9, 1, tzinfo=timezone.utc),
        limit=10,
        quantity=2,
    )

    assert returned is None
    assert session.execute.await_count == 3


@pytest.mark.asyncio
async def test_consume_uses_atomic_limit_condition():
    session = AsyncMock()

    record = make_record(used=9)

    session.execute.side_effect = [
        Mock(),
        make_result(scalar_one_or_none=record),
        make_result(scalar_one_or_none=record.id),
    ]

    session.get.return_value = record

    repository = UsageRepository(session)

    returned = await repository.consume_if_within_limit(
        organisation_id=uuid4(),
        subscription_id=uuid4(),
        resource=UsageResource.API_CALLS,
        period_start=datetime(2026, 8, 1, tzinfo=timezone.utc),
        period_end=datetime(2026, 9, 1, tzinfo=timezone.utc),
        limit=10,
        quantity=1,
    )

    assert returned is record

    update_statement = session.execute.await_args_list[2].args[0]

    compiled = update_statement.compile(
        compile_kwargs={"literal_binds": True},
    )

    sql = str(compiled)

    assert "usage_records.used + 1 <= 10" in sql
    assert "UPDATE usage_records" in sql
    assert "RETURNING usage_records.id" in sql
