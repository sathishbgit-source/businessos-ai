from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.organisation_member import OrganisationMember


class OrganisationMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        member_id: str,
    ) -> OrganisationMember | None:
        result = await self.db.execute(
            select(OrganisationMember).where(
                OrganisationMember.id == member_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_organisation_and_user(
        self,
        organisation_id: str,
        user_id: str,
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
        organisation_id: str,
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
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def update(
        self,
        member: OrganisationMember,
    ) -> OrganisationMember:
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def delete(
        self,
        member: OrganisationMember,
    ) -> None:
        await self.db.delete(member)
        await self.db.commit()