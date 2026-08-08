from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.invitation import (
    get_accept_invitation_service,
    get_get_invitation_service,
    get_invite_member_service,
    get_revoke_invitation_service,
)
from app.schemas.invitation import (
    InvitationAccept,
    InvitationCreate,
    InvitationResponse,
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

router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"],
)


@router.post(
    "/organisations/{organisation_id}",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
)
async def invite_member(
    organisation_id: UUID,
    request: InvitationCreate,
    current_user: User = Depends(get_current_user),
    service: InviteMemberService = Depends(
        get_invite_member_service,
    ),
):
    """Invite a user to an organisation."""

    token = await service.execute(
        organisation_id=organisation_id,
        role_name=request.role,
        email=request.email,
        invited_by=current_user.id,
    )

    return token


@router.get(
    "/{token}",
    response_model=InvitationResponse,
)
async def get_invitation(
    token: str,
    service: GetInvitationService = Depends(
        get_get_invitation_service,
    ),
):
    """Retrieve an invitation."""

    invitation = await service.execute(
        token=token,
    )

    return InvitationResponse(
        id=invitation.id,
        organisation_id=invitation.organisation_id,
        email=invitation.email,
        role=invitation.role.name,
        status=invitation.status,
        expires_at=invitation.expires_at,
        created_at=invitation.created_at,
    )


@router.post(
    "/accept",
    status_code=status.HTTP_200_OK,
)
async def accept_invitation(
    request: InvitationAccept,
    current_user: User = Depends(get_current_user),
    service: AcceptInvitationService = Depends(
        get_accept_invitation_service,
    ),
):
    """Accept an invitation."""

    return await service.execute(
        token=request.token,
        user_id=current_user.id,
    )


@router.delete(
    "/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def revoke_invitation(
    invitation_id: UUID,
    service: RevokeInvitationService = Depends(
        get_revoke_invitation_service,
    ),
):
    """Revoke an invitation."""

    await service.execute(
        invitation_id=invitation_id,
    )