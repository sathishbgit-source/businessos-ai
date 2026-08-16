import pytest

from app.providers.payment.mock import MockPaymentProvider
from app.providers.payment.registry import PaymentProviderRegistry


def test_register_and_resolve_provider():
    registry = PaymentProviderRegistry()

    registry.register("mock", MockPaymentProvider)

    provider = registry.get("mock")

    assert isinstance(provider, MockPaymentProvider)


def test_provider_names_are_case_insensitive():
    registry = PaymentProviderRegistry()

    registry.register("Mock", MockPaymentProvider)

    assert registry.has("mock")
    assert registry.has("MOCK")


def test_unknown_provider_raises_error():
    registry = PaymentProviderRegistry()

    with pytest.raises(
        ValueError,
        match="Payment provider 'unknown' is not registered",
    ):
        registry.get("unknown")


def test_empty_provider_name_is_rejected():
    registry = PaymentProviderRegistry()

    with pytest.raises(
        ValueError,
        match="Payment provider name cannot be empty",
    ):
        registry.register("   ", MockPaymentProvider)


def test_duplicate_provider_registration_is_rejected():
    registry = PaymentProviderRegistry()

    registry.register("mock", MockPaymentProvider)

    with pytest.raises(
        ValueError,
        match="Payment provider 'mock' is already registered",
    ):
        registry.register("MOCK", MockPaymentProvider)
