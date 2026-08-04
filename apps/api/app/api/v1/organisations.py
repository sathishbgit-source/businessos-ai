from fastapi import APIRouter, Depends, status

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.organisation import (
    get_create_organisation_service,
)
from app.schemas.organisation import (
    OrganisationCreate,
    OrganisationResponse,
)
from app.services.organisation.create_organisation import (
    CreateOrganisationService,
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