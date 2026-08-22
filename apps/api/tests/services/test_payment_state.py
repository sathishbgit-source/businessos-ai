import pytest

from app.core.exceptions import PaymentStateTransitionDenied
from app.db.enums import PaymentStatus
from app.services.payment.payment_state import PaymentStateService


@pytest.mark.parametrize(
    ("current_status", "requested_status"),
    [
        (PaymentStatus.PENDING, PaymentStatus.PROCESSING),
        (PaymentStatus.PENDING, PaymentStatus.CANCELLED),
        (PaymentStatus.PROCESSING, PaymentStatus.SUCCEEDED),
        (PaymentStatus.PROCESSING, PaymentStatus.FAILED),
        (PaymentStatus.SUCCEEDED, PaymentStatus.REFUNDED),
    ],
)
def test_valid_payment_transitions(
    current_status,
    requested_status,
):
    PaymentStateService.validate_transition(
        current_status=current_status,
        requested_status=requested_status,
    )


@pytest.mark.parametrize(
    ("current_status", "requested_status"),
    [
        (PaymentStatus.PENDING, PaymentStatus.SUCCEEDED),
        (PaymentStatus.PENDING, PaymentStatus.FAILED),
        (PaymentStatus.PENDING, PaymentStatus.REFUNDED),
        (PaymentStatus.PROCESSING, PaymentStatus.CANCELLED),
        (PaymentStatus.SUCCEEDED, PaymentStatus.PENDING),
        (PaymentStatus.SUCCEEDED, PaymentStatus.FAILED),
        (PaymentStatus.FAILED, PaymentStatus.SUCCEEDED),
        (PaymentStatus.CANCELLED, PaymentStatus.PROCESSING),
        (PaymentStatus.REFUNDED, PaymentStatus.SUCCEEDED),
    ],
)
def test_invalid_payment_transitions(
    current_status,
    requested_status,
):
    with pytest.raises(
        PaymentStateTransitionDenied,
        match="Payment cannot transition",
    ):
        PaymentStateService.validate_transition(
            current_status=current_status,
            requested_status=requested_status,
        )


@pytest.mark.parametrize(
    "status",
    list(PaymentStatus),
)
def test_same_payment_status_is_allowed(status):
    PaymentStateService.validate_transition(
        current_status=status,
        requested_status=status,
    )
