from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.invitation_repository import (
    InvitationRepository,
)
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.organisation_repository import (
    OrganisationRepository,
)
from app.repositories.role_repository import (
    RoleRepository,
)
from app.repositories.user_repository import (
    UserRepository,
)
from app.services.invitation.accept_invitation import (
    AcceptInvitationService,
)
from app.services.invitation.get_invitation import (
    GetInvitationService,
)
from app.services.invitation.invite_member import (
    InviteMemberService,
)
from app.services.invitation.revoke_invitation import (
    RevokeInvitationService,
)


def get_invite_member_service(
    db: AsyncSession = Depends(get_db),
) -> InviteMemberService:
    """Create InviteMemberService with all dependencies."""

    return InviteMemberService(
        db=db,
        invitation_repository=InvitationRepository(db),
        organisation_repository=OrganisationRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
        role_repository=RoleRepository(db),
        user_repository=UserRepository(db),
    )


def get_get_invitation_service(
    db: AsyncSession = Depends(get_db),
) -> GetInvitationService:
    """Create GetInvitationService."""

    return GetInvitationService(
        db=db,
        invitation_repository=InvitationRepository(db),
    )


def get_accept_invitation_service(
    db: AsyncSession = Depends(get_db),
) -> AcceptInvitationService:
    """Create AcceptInvitationService."""

    return AcceptInvitationService(
        db=db,
        invitation_repository=InvitationRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
        user_repository=UserRepository(db),
    )


def get_revoke_invitation_service(
    db: AsyncSession = Depends(get_db),
) -> RevokeInvitationService:
    """Create RevokeInvitationService."""

    return RevokeInvitationService(
        db=db,
        invitation_repository=InvitationRepository(db),
    )