from enum import Enum


class MemberStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    REMOVED = "REMOVED"