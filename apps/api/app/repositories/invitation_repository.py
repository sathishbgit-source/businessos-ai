from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.invitation import Invitation


class InvitationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        invitation_id: str,
    ) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.id == invitation_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_token(
        self,
        token: str,
    ) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.token == token
            )
        )
        return result.scalar_one_or_none()

    async def get_pending_by_email(
        self,
        email: str,
    ) -> list[Invitation]:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.email == email,
                Invitation.status == "PENDING",
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        invitation: Invitation,
    ) -> Invitation:
        self.db.add(invitation)
        await self.db.commit()
        await self.db.refresh(invitation)
        return invitation

    async def update(
        self,
        invitation: Invitation,
    ) -> Invitation:
        await self.db.commit()
        await self.db.refresh(invitation)
        return invitation

    async def delete(
        self,
        invitation: Invitation,
    ) -> None:
        await self.db.delete(invitation)
        await self.db.commit()