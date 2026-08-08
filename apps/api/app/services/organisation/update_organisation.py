from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    OrganisationAccessDenied,
    OrganisationNotFound,
)
from app.db.models.organisation import Organisation
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.organisation_repository import (
    OrganisationRepository,
)


class UpdateOrganisationService:
    """Service responsible for updating organisation settings."""

    def __init__(
        self,
        db: AsyncSession,
        organisation_repository: OrganisationRepository,
        organisation_member_repository: OrganisationMemberRepository,
    ) -> None:
        self.db = db
        self.organisation_repository = organisation_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )

    async def execute(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
        name: str | None = None,
        description: str | None = None,
        logo_url: str | None = None,
        website: str | None = None,
        industry: str | None = None,
        country: str | None = None,
        timezone: str | None = None,
    ) -> Organisation:
        """Update organisation settings."""

        organisation = await self.organisation_repository.get_by_id(
            organisation_id
        )

        if organisation is None:
            raise OrganisationNotFound(
                f"Organisation with id '{organisation_id}' does not exist."
            )

        await self._validate_access(
            organisation_id=organisation_id,
            user_id=user_id,
        )

        updates = {
            "name": name,
            "description": description,
            "logo_url": logo_url,
            "website": website,
            "industry": industry,
            "country": country,
            "timezone": timezone,
        }

        for field, value in updates.items():
            if value is not None:
                setattr(organisation, field, value)

        organisation = await self.organisation_repository.update(
            organisation
        )

        await self.db.commit()
        await self.db.refresh(organisation)

        return organisation

    async def _validate_access(
        self,
        *,
        organisation_id: UUID,
        user_id: UUID,
    ) -> None:
        """Ensure the user is an organisation administrator."""

        member = (
            await self.organisation_member_repository
            .get_by_organisation_and_user(
                organisation_id=organisation_id,
                user_id=user_id,
            )
        )

        if (
            member is None
            or member.status.value != "active"
            or member.role.name != "Administrator"
        ):
            raise OrganisationAccessDenied(
                "User is not authorised to update this organisation."
            )
