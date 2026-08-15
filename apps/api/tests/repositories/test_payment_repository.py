from unittest.mock import AsyncMock, Mock

import pytest

from app.repositories.payment_repository import PaymentRepository


def make_result(items=None, scalar=None):
    result = Mock()

    scalars = Mock()
    scalars.all.return_value = items or []
    result.scalars.return_value = scalars

    result.scalar_one_or_none.return_value = scalar

    return result


@pytest.mark.asyncio
async def test_get_by_provider_payment_id_filters_by_provider_and_reference():
    session = AsyncMock()

    payment = Mock()
    result = make_result(scalar=payment)

    session.execute.return_value = result

    repository = PaymentRepository(session)

    returned_payment = await repository.get_by_provider_payment_id(
        provider="stripe",
        provider_payment_id="pi_123",
    )

    assert returned_payment is payment
    session.execute.assert_awaited_once()

    statement = session.execute.await_args.args[0]

    compiled = statement.compile(
        compile_kwargs={"literal_binds": True},
    )

    sql = str(compiled)

    assert "payments.provider" in sql
    assert "payments.provider_payment_id" in sql
    assert "stripe" in sql
    assert "pi_123" in sql


@pytest.mark.asyncio
async def test_get_by_provider_payment_id_returns_none_when_not_found():
    session = AsyncMock()

    result = make_result(scalar=None)
    session.execute.return_value = result

    repository = PaymentRepository(session)

    returned_payment = await repository.get_by_provider_payment_id(
        provider="razorpay",
        provider_payment_id="pay_123",
    )

    assert returned_payment is None
    session.execute.assert_awaited_once()
