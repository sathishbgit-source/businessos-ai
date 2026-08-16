from abc import ABC, abstractmethod
from decimal import Decimal

from app.providers.payment.models import PaymentProviderResult


class PaymentProvider(ABC):
    """Provider-neutral contract for payment integrations."""

    @abstractmethod
    async def create_payment(
        self,
        *,
        amount: Decimal,
        currency: str,
        payment_id: str,
    ) -> PaymentProviderResult:
        """Create a payment with the provider."""

    @abstractmethod
    async def get_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> PaymentProviderResult:
        """Retrieve a payment from the provider."""

    @abstractmethod
    async def verify_payment(
        self,
        *,
        provider_payment_id: str,
    ) -> PaymentProviderResult:
        """Verify payment state with the provider."""

    @abstractmethod
    async def refund_payment(
        self,
        *,
        provider_payment_id: str,
        amount: Decimal | None = None,
    ) -> PaymentProviderResult:
        """Refund a provider payment."""

    @abstractmethod
    async def handle_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> PaymentProviderResult:
        """Validate and process a provider webhook."""
