from app.core.exceptions import PaymentStateTransitionDenied
from app.db.enums import PaymentStatus


class PaymentStateService:
    """Validate payment lifecycle state transitions."""

    ALLOWED_TRANSITIONS = {
        PaymentStatus.PENDING: {
            PaymentStatus.PROCESSING,
            PaymentStatus.CANCELLED,
        },
        PaymentStatus.PROCESSING: {
            PaymentStatus.SUCCEEDED,
            PaymentStatus.FAILED,
        },
        PaymentStatus.SUCCEEDED: {
            PaymentStatus.REFUNDED,
        },
        PaymentStatus.FAILED: set(),
        PaymentStatus.CANCELLED: set(),
        PaymentStatus.REFUNDED: set(),
    }

    @classmethod
    def validate_transition(
        cls,
        *,
        current_status: PaymentStatus,
        requested_status: PaymentStatus,
    ) -> None:
        """Validate that a payment follows the allowed lifecycle."""

        if current_status == requested_status:
            return

        allowed_statuses = cls.ALLOWED_TRANSITIONS[current_status]

        if requested_status in allowed_statuses:
            return

        raise PaymentStateTransitionDenied(
            f"Payment cannot transition from "
            f"'{current_status.value}' to "
            f"'{requested_status.value}'."
        )
