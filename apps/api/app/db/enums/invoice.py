from enum import Enum


class InvoiceStatus(str, Enum):
    """Lifecycle state for invoices."""

    DRAFT = "DRAFT"
    ISSUED = "ISSUED"
    PAID = "PAID"
    VOID = "VOID"
