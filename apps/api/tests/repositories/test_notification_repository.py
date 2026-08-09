from unittest.mock import AsyncMock, Mock

import pytest

from app.repositories.notification_repository import NotificationRepository


def make_result(total=None, items=None):
    result = Mock()

    if total is not None:
        result.scalar_one.return_value = total

    scalars = Mock()
    scalars.all.return_value = items or []
    result.scalars.return_value = scalars

    return result


@pytest.mark.asyncio
async def test_list_for_user_applies_pagination():
    session = AsyncMock()

    count_result = make_result(total=45)
    data_result = make_result(items=[])

    session.execute.side_effect = [
        count_result,
        data_result,
    ]

    repository = NotificationRepository(session)

    notifications, total = await repository.list_for_user(
        user_id="user-id",
        offset=20,
        limit=20,
    )

    assert notifications == []
    assert total == 45
    assert session.execute.await_count == 2


@pytest.mark.asyncio
async def test_list_for_user_applies_unread_filter():
    session = AsyncMock()

    count_result = make_result(total=10)
    data_result = make_result(items=[])

    session.execute.side_effect = [
        count_result,
        data_result,
    ]

    repository = NotificationRepository(session)

    notifications, total = await repository.list_for_user(
        user_id="user-id",
        unread_only=True,
        offset=0,
        limit=20,
    )

    assert notifications == []
    assert total == 10
    assert session.execute.await_count == 2


@pytest.mark.asyncio
async def test_list_for_user_applies_organisation_filter():
    session = AsyncMock()

    count_result = make_result(total=5)
    data_result = make_result(items=[])

    session.execute.side_effect = [
        count_result,
        data_result,
    ]

    repository = NotificationRepository(session)

    notifications, total = await repository.list_for_user(
        user_id="user-id",
        organisation_id="organisation-id",
        offset=40,
        limit=20,
    )

    assert notifications == []
    assert total == 5
    assert session.execute.await_count == 2


@pytest.mark.asyncio
async def test_list_for_user_returns_empty_page():
    session = AsyncMock()

    count_result = make_result(total=0)
    data_result = make_result(items=[])

    session.execute.side_effect = [
        count_result,
        data_result,
    ]

    repository = NotificationRepository(session)

    notifications, total = await repository.list_for_user(
        user_id="user-id",
        offset=100,
        limit=20,
    )

    assert notifications == []
    assert total == 0
    assert session.execute.await_count == 2
