from datetime import datetime, UTC

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvitationAlreadyAccepted,
    InvitationExpired,
    InvitationNotFound,
    InvitationRevoked,
)
from app.core.security.invitation_tokens import hash_token
from app.db.enums import InvitationStatus
from app.db.models.invitation import Invitation
from app.repositories.invitation_repository import (
    InvitationRepository,
)


class GetInvitationService:
    """Service responsible for retrieving and validating invitations."""

    def __init__(
        self,
        db: AsyncSession,
        invitation_repository: InvitationRepository,
    ) -> None:
        self.db = db
        self.invitation_repository = invitation_repository

    async def execute(
        self,
        *,
        token: str,
    ) -> Invitation:
        """Return a validated invitation."""

        token_hash = hash_token(token)

        invitation = await self._load_invitation(
            token_hash
        )

        self._validate_status(invitation)

        self._validate_expiration(invitation)

        return invitation

    async def _load_invitation(
        self,
        token_hash: str,
    ) -> Invitation:
        """Load invitation using its hashed token."""

        invitation = (
            await self.invitation_repository.get_by_token_hash(
                token_hash
            )
        )

        if invitation is None:
            raise InvitationNotFound(
                "Invitation does not exist."
            )

        return invitation

    def _validate_status(
        self,
        invitation: Invitation,
    ) -> None:
        """Validate invitation status."""

        if invitation.status == InvitationStatus.ACCEPTED:
            raise InvitationAlreadyAccepted(
                "Invitation has already been accepted."
            )

        if invitation.status == InvitationStatus.REVOKED:
            raise InvitationRevoked(
                "Invitation has been revoked."
            )

        if invitation.status == InvitationStatus.EXPIRED:
            raise InvitationExpired(
                "Invitation has expired."
            )

    def _validate_expiration(
        self,
        invitation: Invitation,
    ) -> None:
        """Validate invitation expiry."""

        now = datetime.now(UTC)

        expires_at = invitation.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(
                tzinfo=UTC
            )

        if expires_at < now:
            raise InvitationExpired(
                "Invitation has expired."
            )