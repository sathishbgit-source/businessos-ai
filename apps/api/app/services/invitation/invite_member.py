from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvitationAlreadyExists,
    OrganisationMemberAlreadyExists,
    OrganisationNotFound,
    RoleNotFound,
)
from app.core.security.invitation_tokens import (
    generate_token,
    hash_token,
)
from app.db.models.invitation import Invitation
from app.repositories.invitation_repository import (
    InvitationRepository,
)
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.organisation_repository import (
    OrganisationRepository,
)
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository

class InviteMemberService:
    """Service responsible for inviting users to an organisation."""

    def __init__(
        self,
        db: AsyncSession,
        invitation_repository: InvitationRepository,
        organisation_repository: OrganisationRepository,
        organisation_member_repository: OrganisationMemberRepository,
        role_repository: RoleRepository,
        user_repository: UserRepository,
    ) -> None:
        self.db = db
        self.invitation_repository = invitation_repository
        self.organisation_repository = organisation_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )
        self.role_repository = role_repository
        self.user_repository = user_repository

    async def execute(
        self,
        *,
        organisation_id,
        role_id,
        email: str,
        invited_by,
    ) -> str:


        """Create an invitation and return the raw invitation token."""

        organisation = await self._load_organisation(
            organisation_id
        )

        role = await self._load_role(
            role_id
        )

        normalized_email = self._normalize_email(
            email
        )

        await self._validate_existing_member(
            organisation_id=organisation.id,
            email=normalized_email,
        )

        await self._validate_pending_invitation(
            organisation_id=organisation.id,
            email=normalized_email,
        )

        raw_token = generate_token()
        token_hash = hash_token(raw_token)

        invitation = Invitation(
            organisation_id=organisation.id,
            role_id=role.id,
            email=normalized_email,
            token_hash=token_hash,
            created_by=invited_by,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )

        await self.invitation_repository.create(
            invitation
        )

        await self.db.commit()

        return raw_token
    async def _load_organisation(
        self,
        organisation_id,
    ):
        """Load organisation."""

        organisation = await (
            self.organisation_repository.get_by_id(
                organisation_id
            )
        )

        if organisation is None:
            raise OrganisationNotFound(
                f"Organisation '{organisation_id}' does not exist."
            )

        return organisation

    async def _load_role(
        self,
        role_id,
    ):
        """Load invitation role."""

        role = await self.role_repository.get_by_id(
            role_id
        )

        if role is None:
            raise RoleNotFound(
                f"Role '{role_id}' does not exist."
            )

        return role

    def _normalize_email(
        self,
        email: str,
    ) -> str:
        """Normalize email."""

        return email.strip().lower()

    async def _validate_existing_member(
        self,
        *,
        organisation_id,
        email: str,
    ) -> None:
       
        """Ensure the invited user is not already an organisation member."""

        user = await self.user_repository.get_by_email(
            email
        )

        if user is None:
            return

        member = (
            await self.organisation_member_repository.get_by_organisation_and_user(
                organisation_id,
                user.id,
            )
        )

        if member is not None:
            raise OrganisationMemberAlreadyExists(
                f"User '{email}' is already a member of this organisation."
            )

    async def _validate_pending_invitation(
        self,
        *,
        organisation_id,
        email: str,
    ) -> None:
        """Ensure there is no active pending invitation."""

        invitations = (
            await self.invitation_repository.get_pending_by_email_and_organisation(
                organisation_id,
                email,
            )
        )

        if invitations:
            raise InvitationAlreadyExists(
                f"A pending invitation already exists for '{email}'."
            )