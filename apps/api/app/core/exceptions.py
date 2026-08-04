"""Application exception hierarchy."""


class BusinessOSError(Exception):
    """Base exception for all business rule violations."""


class OrganisationAlreadyExists(BusinessOSError):
    """Raised when an organisation slug already exists."""


class UserNotFound(BusinessOSError):
    """Raised when the specified user does not exist."""


class RoleNotFound(BusinessOSError):
    """Raised when the required role does not exist."""