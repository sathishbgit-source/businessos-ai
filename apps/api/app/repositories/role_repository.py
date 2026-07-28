from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.role import Role


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, role_id: str) -> Role | None:
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Role | None:
        result = await self.db.execute(
            select(Role).where(Role.name == name)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Role]:
        result = await self.db.execute(
            select(Role).order_by(Role.name)
        )
        return list(result.scalars().all())

    async def create(self, role: Role) -> Role:
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def update(self, role: Role) -> Role:
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def delete(self, role: Role) -> None:
        await self.db.delete(role)
        await self.db.commit()