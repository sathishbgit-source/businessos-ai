from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.enums import InvitationStatus
from app.db.models.invitation import Invitation


class InvitationRepository:
    """Repository responsible for Invitation persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        invitation_id: UUID,
    ) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.id == invitation_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_token_hash(
        self,
        token_hash: str,
    ) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation)
            .options(
                selectinload(Invitation.role)
            )
            .where(
                Invitation.token_hash == token_hash
            )
        )

        return result.scalar_one_or_none()

    async def get_pending_by_email_and_organisation(
        self,
        organisation_id: UUID,
        email: str,
    ) -> list[Invitation]:
        """
        Return pending invitations for an email within
        a specific organisation.
        """
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.organisation_id == organisation_id,
                Invitation.email == email,
                Invitation.status == InvitationStatus.PENDING,
            )
        )

        return list(result.scalars().all())

    async def create(
        self,
        invitation: Invitation,
    ) -> Invitation:
        """
        Persist a new invitation.

        Transaction commit is handled by the service layer.
        """
        self.db.add(invitation)
        await self.db.flush()
        await self.db.refresh(invitation)

        return invitation

    async def update(
        self,
        invitation: Invitation,
    ) -> Invitation:
        """
        Flush pending invitation changes.

        Commit is handled by the service layer.
        """
        await self.db.flush()
        await self.db.refresh(invitation)

        return invitation

    async def delete(
        self,
        invitation: Invitation,
    ) -> None:
        """
        Remove an invitation.

        Commit is handled by the service layer.
        """
        await self.db.delete(invitation)
        await self.db.flush()