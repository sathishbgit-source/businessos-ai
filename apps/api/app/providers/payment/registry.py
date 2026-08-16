from collections.abc import Callable

from app.providers.payment.base import PaymentProvider


PaymentProviderFactory = Callable[[], PaymentProvider]


class PaymentProviderRegistry:
    """Registry for resolving configured payment providers."""

    def __init__(self) -> None:
        self._providers: dict[str, PaymentProviderFactory] = {}

    def register(
        self,
        name: str,
        factory: PaymentProviderFactory,
    ) -> None:
        """Register a payment provider factory."""

        provider_name = name.strip().lower()

        if not provider_name:
            raise ValueError("Payment provider name cannot be empty.")

        if provider_name in self._providers:
            raise ValueError(
                f"Payment provider '{provider_name}' is already registered."
            )

        self._providers[provider_name] = factory

    def get(self, name: str) -> PaymentProvider:
        """Resolve a registered payment provider."""

        provider_name = name.strip().lower()

        if provider_name not in self._providers:
            raise ValueError(
                f"Payment provider '{provider_name}' is not registered."
            )

        return self._providers[provider_name]()

    def has(self, name: str) -> bool:
        """Return whether a provider is registered."""

        return name.strip().lower() in self._providers
