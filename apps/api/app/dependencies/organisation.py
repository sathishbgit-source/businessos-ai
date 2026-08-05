from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.organisation_repository import (
    OrganisationRepository,
)
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.organisation.create_organisation import (
    CreateOrganisationService,
)


def get_create_organisation_service(
    db: AsyncSession = Depends(get_db),
) -> CreateOrganisationService:
    """Create CreateOrganisationService with all dependencies."""

    return CreateOrganisationService(
        db=db,
        organisation_repository=OrganisationRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
        role_repository=RoleRepository(db),
        user_repository=UserRepository(db),
)