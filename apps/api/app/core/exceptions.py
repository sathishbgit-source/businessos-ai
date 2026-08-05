"""Application exception hierarchy."""


class BusinessOSError(Exception):
    """Base exception for all business rule violations."""


class OrganisationAlreadyExists(BusinessOSError):
    """Raised when an organisation slug already exists."""


class UserNotFound(BusinessOSError):
    """Raised when the specified user does not exist."""


class RoleNotFound(BusinessOSError):
    """Raised when the required role does not exist."""

class OrganisationNotFound(BusinessOSError):
    """Raised when the specified organisation does not exist."""


class InvitationAlreadyExists(BusinessOSError):
    """Raised when a pending invitation already exists."""


class OrganisationMemberAlreadyExists(BusinessOSError):
    """Raised when the user is already a member of the organisation."""


class InvitationNotFound(BusinessOSError):
    """Raised when the invitation cannot be found."""


class InvitationExpired(BusinessOSError):
    """Raised when the invitation has expired."""


class InvitationRevoked(BusinessOSError):
    """Raised when the invitation has been revoked."""


class InvitationAlreadyAccepted(BusinessOSError):
    """Raised when the invitation has already been accepted."""