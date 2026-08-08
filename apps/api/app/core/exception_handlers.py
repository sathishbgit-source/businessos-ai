from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    BusinessOSError,
    NotificationAccessDenied,
    NotificationNotFound,
    OrganisationAccessDenied,
    OrganisationAlreadyExists,
    OrganisationNotFound,
    RoleNotFound,
    UserNotFound,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register application exception handlers."""

    @app.exception_handler(OrganisationAlreadyExists)
    async def organisation_exists_handler(
        request: Request,
        exc: OrganisationAlreadyExists,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(OrganisationNotFound)
    async def organisation_not_found_handler(
        request: Request,
        exc: OrganisationNotFound,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(OrganisationAccessDenied)
    async def organisation_access_denied_handler(
        request: Request,
        exc: OrganisationAccessDenied,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotificationNotFound)
    async def notification_not_found_handler(
        request: Request,
        exc: NotificationNotFound,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotificationAccessDenied)
    async def notification_access_denied_handler(
        request: Request,
        exc: NotificationAccessDenied,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFound,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(RoleNotFound)
    async def role_not_found_handler(
        request: Request,
        exc: RoleNotFound,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BusinessOSError)
    async def business_error_handler(
        request: Request,
        exc: BusinessOSError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )
