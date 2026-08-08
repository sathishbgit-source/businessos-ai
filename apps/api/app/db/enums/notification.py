from enum import StrEnum


class NotificationType(StrEnum):
    SYSTEM = "SYSTEM"
    INVITATION = "INVITATION"
    SECURITY = "SECURITY"
    ORGANISATION = "ORGANISATION"
    MEMBER = "MEMBER"
