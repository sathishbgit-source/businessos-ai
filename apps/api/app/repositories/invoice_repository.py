from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.invoice import Invoice
from app.db.models.invoice_line_item import InvoiceLineItem


class InvoiceRepository:
    """Repository responsible for invoice persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        invoice_id: UUID,
    ) -> Invoice | None:
        result = await self.db.execute(
            select(Invoice).where(
                Invoice.id == invoice_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_billing_record(
        self,
        billing_record_id: UUID,
    ) -> Invoice | None:
        result = await self.db.execute(
            select(Invoice).where(
                Invoice.billing_record_id == billing_record_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_invoice_number(
        self,
        invoice_number: str,
    ) -> Invoice | None:
        result = await self.db.execute(
            select(Invoice).where(
                Invoice.invoice_number == invoice_number
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_organisation(
        self,
        organisation_id: UUID,
    ) -> list[Invoice]:
        result = await self.db.execute(
            select(Invoice)
            .where(
                Invoice.organisation_id == organisation_id
            )
            .order_by(Invoice.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        invoice: Invoice,
    ) -> Invoice:
        self.db.add(invoice)
        await self.db.flush()
        await self.db.refresh(invoice)

        return invoice

    async def create_line_item(
        self,
        line_item: InvoiceLineItem,
    ) -> InvoiceLineItem:
        self.db.add(line_item)
        await self.db.flush()
        await self.db.refresh(line_item)

        return line_item

    async def get_line_items(
        self,
        invoice_id: UUID,
    ) -> list[InvoiceLineItem]:
        result = await self.db.execute(
            select(InvoiceLineItem)
            .where(
                InvoiceLineItem.invoice_id == invoice_id
            )
            .order_by(InvoiceLineItem.created_at.asc())
        )
        return list(result.scalars().all())

    async def update(
        self,
        invoice: Invoice,
    ) -> Invoice:
        await self.db.flush()
        await self.db.refresh(invoice)

        return invoice
