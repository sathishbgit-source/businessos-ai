from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.organisation_member import OrganisationMember


class OrganisationMemberRepository:
    """Repository responsible for OrganisationMember persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        member_id: UUID,
    ) -> OrganisationMember | None:
        result = await self.db.execute(
            select(OrganisationMember).where(
                OrganisationMember.id == member_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_organisation_and_user(
        self,
        organisation_id: UUID,
        user_id: UUID,
    ) -> OrganisationMember | None:
        result = await self.db.execute(
            select(OrganisationMember).where(
                OrganisationMember.organisation_id == organisation_id,
                OrganisationMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_organisation(
        self,
        organisation_id: UUID,
    ) -> list[OrganisationMember]:
        result = await self.db.execute(
            select(OrganisationMember).where(
                OrganisationMember.organisation_id == organisation_id
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        member: OrganisationMember,
    ) -> OrganisationMember:
        """
        Persist a new organisation member.

        Transaction commit is handled by the service layer.
        """
        self.db.add(member)
        await self.db.flush()
        await self.db.refresh(member)

        return member

    async def update(
        self,
        member: OrganisationMember,
    ) -> OrganisationMember:
        """
        Flush pending member changes.

        Commit is handled by the service layer.
        """
        await self.db.flush()
        await self.db.refresh(member)

        return member

    async def delete(
        self,
        member: OrganisationMember,
    ) -> None:
        """
        Remove a member.

        Commit is handled by the service layer.
        """
        await self.db.delete(member)
        await self.db.flush()