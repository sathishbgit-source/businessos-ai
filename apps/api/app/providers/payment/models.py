from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.db.enums import PaymentStatus


@dataclass(frozen=True)
class PaymentProviderResult:
    """Provider-neutral result returned by payment operations."""

    provider_payment_id: str
    status: PaymentStatus
    amount: Decimal | None = None
    currency: str | None = None
    failure_reason: str | None = None
    paid_at: datetime | None = None
