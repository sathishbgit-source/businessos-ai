from enum import Enum


class BillingStatus(str, Enum):
    PENDING = "PENDING"
    BILLED = "BILLED"
    PAID = "PAID"
    FAILED = "FAILED"
