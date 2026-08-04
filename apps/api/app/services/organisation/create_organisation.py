from app.db.models.organisation import Organisation
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.organisation_repository import (
    OrganisationRepository,
)
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository


class CreateOrganisationService:
    """Use case for creating a new organisation."""

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
        """
        Create a new organisation.

        Workflow
        --------
        1. Check slug uniqueness.
        2. Verify owner exists.
        3. Load Administrator role.
        4. Create organisation.
        5. Add owner as first member.
        6. Return created organisation.
        """

        # Step 1 - Check slug uniqueness
        existing = await self.organisation_repository.get_by_slug(slug)

        if existing:
            raise ValueError(
                f"Organisation with slug '{slug}' already exists."
            )

        # Step 2 - Verify owner exists
        owner = await self.user_repository.get_by_id(owner_id)

        if owner is None:
            raise ValueError(
                f"User with id '{owner_id}' does not exist."
            )

        # Step 3 - Load Administrator role
        admin_role = await self.role_repository.get_by_name(
            "Administrator"
        )

        if admin_role is None:
            raise ValueError(
                "Administrator role does not exist."
            )

        # Remaining steps will be implemented next.
        raise NotImplementedError(
            "Organisation creation is not implemented yet."
        )