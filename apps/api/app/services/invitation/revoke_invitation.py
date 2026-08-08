from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvitationAlreadyAccepted,
    InvitationNotFound,
    InvitationRevoked,
)
from app.db.enums import InvitationStatus
from app.db.models.invitation import Invitation
from app.repositories.invitation_repository import (
    InvitationRepository,
)


class RevokeInvitationService:
    """Service responsible for revoking invitations."""

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
        invitation_id,
    ) -> Invitation:
        """Revoke a pending invitation."""

        invitation = await self._load_invitation(
            invitation_id
        )

        self._validate_status(invitation)

        invitation.status = InvitationStatus.REVOKED

        await self.invitation_repository.update(
            invitation
        )

        await self.db.commit()

        return invitation

    async def _load_invitation(
        self,
        invitation_id,
    ) -> Invitation:
        """Load invitation by id."""

        invitation = (
            await self.invitation_repository.get_by_id(
                invitation_id
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
        """Validate invitation can be revoked."""

        if invitation.status == InvitationStatus.ACCEPTED:
            raise InvitationAlreadyAccepted(
                "Invitation has already been accepted."
            )

        if invitation.status == InvitationStatus.REVOKED:
            raise InvitationRevoked(
                "Invitation has already been revoked."
            )