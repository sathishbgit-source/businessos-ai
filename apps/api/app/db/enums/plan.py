from enum import Enum


class BillingInterval(str, Enum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class PlanStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
