from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.permission import Permission


class PermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, permission_id: str) -> Permission | None:
        result = await self.db.execute(
            select(Permission).where(Permission.id == permission_id)
        )
        return result.scalar_one_or_none()

    async def get_by_resource_action(
        self,
        resource: str,
        action: str,
    ) -> Permission | None:
        result = await self.db.execute(
            select(Permission).where(
                Permission.resource == resource,
                Permission.action == action,
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Permission]:
        result = await self.db.execute(
            select(Permission).order_by(
                Permission.resource,
                Permission.action,
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        permission: Permission,
    ) -> Permission:
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        return permission

    async def update(
        self,
        permission: Permission,
    ) -> Permission:
        await self.db.commit()
        await self.db.refresh(permission)
        return permission

    async def delete(
        self,
        permission: Permission,
    ) -> None:
        await self.db.delete(permission)
        await self.db.commit()