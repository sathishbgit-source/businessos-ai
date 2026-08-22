from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.core.exceptions import (
    BillingRecordNotFound,
    InvoiceAlreadyExists,
    PlanNotFound,
)
from app.db.enums import InvoiceStatus
from app.db.models.billing_record import BillingRecord
from app.db.models.invoice import Invoice
from app.services.invoice.create_invoice import CreateInvoiceService


def make_billing_record():
    billing_record = Mock(spec=BillingRecord)
    billing_record.id = uuid4()
    billing_record.organisation_id = uuid4()
    billing_record.customer_id = uuid4()
    billing_record.subscription_id = uuid4()
    billing_record.plan_id = uuid4()
    billing_record.billing_period_start = datetime(
        2026, 2, 15, tzinfo=timezone.utc
    )
    billing_record.billing_period_end = datetime(
        2026, 3, 15, tzinfo=timezone.utc
    )
    billing_record.amount = Decimal("79.00")
    billing_record.currency = "AUD"

    return billing_record


def make_plan():
    plan = Mock()
    plan.id = uuid4()
    plan.name = "Starter"
    plan.price = Decimal("79.00")
    plan.currency = "AUD"

    return plan


def make_service():
    db = AsyncMock()
    billing_repository = Mock()
    invoice_repository = Mock()
    plan_repository = Mock()

    service = CreateInvoiceService(
        db=db,
        billing_repository=billing_repository,
        invoice_repository=invoice_repository,
        plan_repository=plan_repository,
    )

    return (
        service,
        db,
        billing_repository,
        invoice_repository,
        plan_repository,
    )


@pytest.mark.asyncio
async def test_creates_invoice_from_billing_record():
    (
        service,
        db,
        billing_repository,
        invoice_repository,
        plan_repository,
    ) = make_service()

    billing_record = make_billing_record()
    plan = make_plan()

    billing_repository.get_by_id = AsyncMock(
        return_value=billing_record
    )
    invoice_repository.get_by_billing_record = AsyncMock(
        return_value=None
    )
    invoice_repository.create = AsyncMock(
        side_effect=lambda invoice: invoice
    )
    invoice_repository.create_line_item = AsyncMock(
        side_effect=lambda line_item: line_item
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=plan
    )

    due_at = datetime(
        2026, 3, 20, tzinfo=timezone.utc
    )

    result = await service.execute(
        billing_record_id=billing_record.id,
        due_at=due_at,
        payment_reference="pay_123",
    )

    assert isinstance(result, Invoice)
    assert result.organisation_id == billing_record.organisation_id
    assert result.customer_id == billing_record.customer_id
    assert result.subscription_id == billing_record.subscription_id
    assert result.billing_record_id == billing_record.id

    assert result.billing_period_start == (
        billing_record.billing_period_start
    )
    assert result.billing_period_end == (
        billing_record.billing_period_end
    )

    assert result.subtotal == Decimal("79.00")
    assert result.tax == Decimal("0.00")
    assert result.total == Decimal("79.00")
    assert result.currency == "AUD"

    assert result.status == InvoiceStatus.ISSUED
    assert result.payment_reference == "pay_123"
    assert result.due_at == due_at

    assert result.invoice_number.startswith("INV-")

    invoice_repository.create.assert_awaited_once()
    invoice_repository.create_line_item.assert_awaited_once()

    line_item = invoice_repository.create_line_item.await_args.args[0]

    assert line_item.invoice_id == result.id
    assert line_item.description == plan.name
    assert line_item.quantity == Decimal("1")
    assert line_item.unit_amount == Decimal("79.00")
    assert line_item.amount == Decimal("79.00")
    assert line_item.currency == "AUD"

    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_uses_billing_record_amount_not_current_plan_price():
    (
        service,
        _,
        billing_repository,
        invoice_repository,
        plan_repository,
    ) = make_service()

    billing_record = make_billing_record()
    billing_record.amount = Decimal("69.00")

    plan = make_plan()
    plan.price = Decimal("79.00")

    billing_repository.get_by_id = AsyncMock(
        return_value=billing_record
    )
    invoice_repository.get_by_billing_record = AsyncMock(
        return_value=None
    )
    invoice_repository.create = AsyncMock(
        side_effect=lambda invoice: invoice
    )
    invoice_repository.create_line_item = AsyncMock(
        side_effect=lambda line_item: line_item
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=plan
    )

    result = await service.execute(
        billing_record_id=billing_record.id
    )

    assert result.subtotal == Decimal("69.00")
    assert result.total == Decimal("69.00")

    line_item = invoice_repository.create_line_item.await_args.args[0]

    assert line_item.unit_amount == Decimal("69.00")
    assert line_item.amount == Decimal("69.00")


@pytest.mark.asyncio
async def test_rejects_duplicate_invoice():
    (
        service,
        _,
        billing_repository,
        invoice_repository,
        plan_repository,
    ) = make_service()

    billing_record = make_billing_record()
    existing_invoice = Mock(spec=Invoice)

    invoice_repository.get_by_billing_record = AsyncMock(
        return_value=existing_invoice
    )
    billing_repository.get_by_id = AsyncMock()
    plan_repository.get_by_id = AsyncMock()

    with pytest.raises(InvoiceAlreadyExists):
        await service.execute(
            billing_record_id=billing_record.id
        )

    billing_repository.get_by_id.assert_not_awaited()
    plan_repository.get_by_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_rejects_missing_billing_record():
    (
        service,
        _,
        billing_repository,
        invoice_repository,
        plan_repository,
    ) = make_service()

    billing_record_id = uuid4()

    invoice_repository.get_by_billing_record = AsyncMock(
        return_value=None
    )
    billing_repository.get_by_id = AsyncMock(
        return_value=None
    )
    plan_repository.get_by_id = AsyncMock()

    with pytest.raises(BillingRecordNotFound):
        await service.execute(
            billing_record_id=billing_record_id
        )

    plan_repository.get_by_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_rejects_missing_plan():
    (
        service,
        _,
        billing_repository,
        invoice_repository,
        plan_repository,
    ) = make_service()

    billing_record = make_billing_record()

    invoice_repository.get_by_billing_record = AsyncMock(
        return_value=None
    )
    billing_repository.get_by_id = AsyncMock(
        return_value=billing_record
    )
    plan_repository.get_by_id = AsyncMock(
        return_value=None
    )

    with pytest.raises(PlanNotFound):
        await service.execute(
            billing_record_id=billing_record.id
        )

    invoice_repository.create.assert_not_called()
    invoice_repository.create_line_item.assert_not_called()


@pytest.mark.asyncio
async def test_invoice_number_is_unique():
    (
        service,
        _,
        _,
        _,
        _,
    ) = make_service()

    first = service._generate_invoice_number()
    second = service._generate_invoice_number()

    assert first.startswith("INV-")
    assert second.startswith("INV-")
    assert first != second
