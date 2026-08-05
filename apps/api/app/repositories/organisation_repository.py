from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.organisation import Organisation


class OrganisationRepository:
    """Repository responsible for Organisation persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        organisation_id: UUID,
    ) -> Organisation | None:
        result = await self.db.execute(
            select(Organisation).where(
                Organisation.id == organisation_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Organisation | None:
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
        """
        Persist a new organisation.

        Transaction commit is intentionally handled
        by the service layer.
        """
        self.db.add(organisation)

        # Flush assigns generated values (UUID/defaults)
        # without committing the transaction.
        await self.db.flush()
        await self.db.refresh(organisation)

        return organisation

    async def update(
        self,
        organisation: Organisation,
    ) -> Organisation:
        """
        Flush pending changes.

        Transaction commit is handled by the service.
        """
        await self.db.flush()
        await self.db.refresh(organisation)

        return organisation

    async def delete(
        self,
        organisation: Organisation,
    ) -> None:
        """
        Mark entity for deletion.

        Commit is handled by the service.
        """
        await self.db.delete(organisation)
        await self.db.flush()