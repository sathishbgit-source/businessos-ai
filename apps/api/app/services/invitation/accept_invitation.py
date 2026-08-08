from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    OrganisationMemberAlreadyExists,
    UserNotFound,
)
from app.db.enums import InvitationStatus
from app.db.models.organisation_member import OrganisationMember
from app.db.models.user import User
from app.repositories.invitation_repository import (
    InvitationRepository,
)
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.user_repository import UserRepository
from app.services.invitation.get_invitation import (
    GetInvitationService,
)


class AcceptInvitationService:
    """Service responsible for accepting invitations."""

    def __init__(
        self,
        db: AsyncSession,
        invitation_repository: InvitationRepository,
        organisation_member_repository: OrganisationMemberRepository,
        user_repository: UserRepository,
    ) -> None:
        self.db = db
        self.invitation_repository = invitation_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )
        self.user_repository = user_repository

    async def execute(
        self,
        *,
        token: str,
        user_id,
    ) -> OrganisationMember:
        """Accept an invitation."""

        invitation = await GetInvitationService(
            db=self.db,
            invitation_repository=self.invitation_repository,
        ).execute(token=token)

        user = await self._load_user(user_id)

        if user.email.lower() != invitation.email.lower():
            raise UserNotFound(
                "Authenticated user does not match invitation."
            )

        existing = (
            await self.organisation_member_repository.get_by_organisation_and_user(
                invitation.organisation_id,
                user.id,
            )
        )

        if existing is not None:
            raise OrganisationMemberAlreadyExists(
                "User is already a member."
            )

        member = OrganisationMember(
            organisation_id=invitation.organisation_id,
            user_id=user.id,
            role_id=invitation.role_id,
        )

        await self.organisation_member_repository.create(
            member
        )

        invitation.status = InvitationStatus.ACCEPTED
        invitation.accepted_at = datetime.utcnow()

        await self.invitation_repository.update(
            invitation
        )

        await self.db.commit()

        return member

    async def _load_user(
        self,
        user_id,
    ) -> User:
        """Load authenticated user."""

        user = await self.user_repository.get_by_id(
            user_id
        )

        if user is None:
            raise UserNotFound(
                "User does not exist."
            )

        return user