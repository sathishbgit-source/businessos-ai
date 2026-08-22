from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BillingRecordNotFound
from app.core.exceptions import InvoiceAlreadyExists
from app.core.exceptions import PlanNotFound
from app.db.enums import InvoiceStatus
from app.db.models.invoice import Invoice
from app.db.models.invoice_line_item import InvoiceLineItem
from app.repositories.billing_repository import BillingRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.plan_repository import PlanRepository


class CreateInvoiceService:
    """Create an invoice from an existing billing record."""

    def __init__(
        self,
        db: AsyncSession,
        billing_repository: BillingRepository,
        invoice_repository: InvoiceRepository,
        plan_repository: PlanRepository,
    ):
        self.db = db
        self.billing_repository = billing_repository
        self.invoice_repository = invoice_repository
        self.plan_repository = plan_repository

    async def execute(
        self,
        billing_record_id: UUID,
        due_at: datetime | None = None,
        payment_reference: str | None = None,
    ) -> Invoice:
        existing_invoice = (
            await self.invoice_repository.get_by_billing_record(
                billing_record_id
            )
        )

        if existing_invoice is not None:
            raise InvoiceAlreadyExists(
                "An invoice already exists for this billing record."
            )

        billing_record = await self.billing_repository.get_by_id(
            billing_record_id
        )

        if billing_record is None:
            raise BillingRecordNotFound(
                f"Billing record {billing_record_id} was not found."
            )

        plan = await self.plan_repository.get_by_id(
            billing_record.plan_id
        )

        if plan is None:
            raise PlanNotFound(
                f"Plan {billing_record.plan_id} was not found."
            )

        amount = Decimal(str(billing_record.amount))

        invoice = Invoice(
            invoice_number=self._generate_invoice_number(),
            organisation_id=billing_record.organisation_id,
            customer_id=billing_record.customer_id,
            subscription_id=billing_record.subscription_id,
            billing_record_id=billing_record.id,
            billing_period_start=billing_record.billing_period_start,
            billing_period_end=billing_record.billing_period_end,
            subtotal=amount,
            tax=Decimal("0.00"),
            total=amount,
            currency=billing_record.currency,
            status=InvoiceStatus.ISSUED,
            payment_reference=payment_reference,
            due_at=due_at,
        )

        invoice = await self.invoice_repository.create(invoice)

        line_item = InvoiceLineItem(
            invoice_id=invoice.id,
            description=plan.name,
            quantity=Decimal("1"),
            unit_amount=amount,
            amount=amount,
            currency=billing_record.currency,
        )

        await self.invoice_repository.create_line_item(line_item)

        await self.db.commit()
        await self.db.refresh(invoice)

        return invoice

    @staticmethod
    def _generate_invoice_number() -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        suffix = uuid4().hex[:8].upper()

        return f"INV-{timestamp}-{suffix}"
