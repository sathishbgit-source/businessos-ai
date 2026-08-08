from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.organisation import (
    get_create_organisation_service,
    get_update_organisation_service,
)
from app.schemas.organisation import (
    OrganisationCreate,
    OrganisationResponse,
    OrganisationUpdate,
)
from app.services.organisation.create_organisation import (
    CreateOrganisationService,
)
from app.services.organisation.update_organisation import (
    UpdateOrganisationService,
)

router = APIRouter(
    prefix="/organisations",
    tags=["Organisations"],
)


@router.post(
    "",
    response_model=OrganisationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organisation(
    request: OrganisationCreate,
    current_user: User = Depends(get_current_user),
    service: CreateOrganisationService = Depends(
        get_create_organisation_service,
    ),
):
    """Create a new organisation."""

    organisation = await service.execute(
        name=request.name,
        slug=request.slug,
        description=request.description,
        owner_id=current_user.id,
    )

    return OrganisationResponse.model_validate(
        organisation
    )

@router.patch(
    "/{organisation_id}",
    response_model=OrganisationResponse,
    status_code=status.HTTP_200_OK,
)
async def update_organisation(
    organisation_id: UUID,
    request: OrganisationUpdate,
    current_user: User = Depends(get_current_user),
    service: UpdateOrganisationService = Depends(
        get_update_organisation_service,
    ),
):
    """Update organisation settings."""

    organisation = await service.execute(
        organisation_id=organisation_id,
        user_id=current_user.id,
        name=request.name,
        description=request.description,
        logo_url=request.logo_url,
        website=request.website,
        industry=request.industry,
        country=request.country,
        timezone=request.timezone,
    )

    return OrganisationResponse.model_validate(
        organisation
    )
