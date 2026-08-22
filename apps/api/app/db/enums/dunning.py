from enum import Enum


class DunningStatus(str, Enum):
    """Lifecycle state for failed-payment recovery."""

    RETRYING = "RETRYING"
    GRACE_PERIOD = "GRACE_PERIOD"
    RECOVERED = "RECOVERED"
    SUSPENDED = "SUSPENDED"
