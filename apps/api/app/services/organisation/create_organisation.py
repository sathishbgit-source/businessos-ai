from app.core.exceptions import (
    OrganisationAlreadyExists,
    RoleNotFound,
    UserNotFound,
)
from app.db.models.organisation import Organisation
from app.db.models.organisation_member import OrganisationMember
from app.db.models.role import Role
from app.db.models.user import User
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.organisation_repository import (
    OrganisationRepository,
)
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository


class CreateOrganisationService:
    """Service responsible for creating an organisation."""

    def __init__(
        self,
        organisation_repository: OrganisationRepository,
        organisation_member_repository: OrganisationMemberRepository,
        role_repository: RoleRepository,
        user_repository: UserRepository,
    ) -> None:
        self.organisation_repository = organisation_repository
        self.organisation_member_repository = (
            organisation_member_repository
        )
        self.role_repository = role_repository
        self.user_repository = user_repository

    async def execute(
        self,
        *,
        name: str,
        slug: str,
        description: str | None,
        owner_id: str,
    ) -> Organisation:
        """Execute the create organisation workflow."""

        await self._validate_slug(slug)

        owner = await self._load_owner(owner_id)

        admin_role = await self._load_admin_role()

        organisation = await self._create_organisation(
            name=name,
            slug=slug,
            description=description,
            owner_id=owner.id,
        )

        await self._assign_owner(
            organisation=organisation,
            owner=owner,
            role=admin_role,
        )

        return organisation

    async def _validate_slug(
        self,
        slug: str,
    ) -> None:
        """Ensure organisation slug is unique."""

        existing = await self.organisation_repository.get_by_slug(
            slug
        )

        if existing:
            raise OrganisationAlreadyExists(
                f"Organisation with slug '{slug}' already exists."
            )

    async def _load_owner(
        self,
        owner_id: str,
    ) -> User:
        """Load organisation owner."""

        owner = await self.user_repository.get_by_id(owner_id)

        if owner is None:
            raise UserNotFound(
                f"User with id '{owner_id}' does not exist."
            )

        return owner

    async def _load_admin_role(
        self,
    ) -> Role:
        """Load administrator role."""

        admin_role = await self.role_repository.get_by_name(
            "Administrator"
        )

        if admin_role is None:
            raise RoleNotFound(
                "Administrator role does not exist."
            )

        return admin_role

    async def _create_organisation(
        self,
        *,
        name: str,
        slug: str,
        description: str | None,
        owner_id,
    ) -> Organisation:
        """Create the organisation."""

        organisation = Organisation(
            name=name,
            slug=slug,
            description=description,
            owner_id=owner_id,
        )

        return await self.organisation_repository.create(
            organisation
        )

    async def _assign_owner(
        self,
        *,
        organisation: Organisation,
        owner: User,
        role: Role,
    ) -> None:
        """Assign the creator as the first organisation member."""

        member = OrganisationMember(
            organisation_id=organisation.id,
            user_id=owner.id,
            role_id=role.id,
        )

        await self.organisation_member_repository.create(
            member
        )