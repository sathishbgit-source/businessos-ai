from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.organisation import Organisation


class OrganisationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, organisation_id: str) -> Organisation | None:
        result = await self.db.execute(
            select(Organisation).where(
                Organisation.id == organisation_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Organisation | None:
        result = await self.db.execute(
            select(Organisation).where(
                Organisation.slug == slug
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Organisation]:
        result = await self.db.execute(
            select(Organisation).order_by(
                Organisation.name
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        organisation: Organisation,
    ) -> Organisation:
        self.db.add(organisation)
        await self.db.commit()
        await self.db.refresh(organisation)
        return organisation

    async def update(
        self,
        organisation: Organisation,
    ) -> Organisation:
        await self.db.commit()
        await self.db.refresh(organisation)
        return organisation

    async def delete(
        self,
        organisation: Organisation,
    ) -> None:
        await self.db.delete(organisation)
        await self.db.commit()