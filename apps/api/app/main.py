from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.v1.router import router as api_v1_router
from app.config import settings
from app.core.exception_handlers import (
    register_exception_handlers,
)
from app.middleware.rate_limit import RateLimitMiddleware


openapi_tags = [
    {
        "name": "Health",
        "description": "API health and service status endpoints.",
    },
    {
        "name": "Authentication",
        "description": (
            "User registration, authentication, and current-user endpoints."
        ),
    },
    {
        "name": "Organisations",
        "description": "Organisation creation and management endpoints.",
    },
    {
        "name": "Invitations",
        "description": "Organisation member invitation lifecycle endpoints.",
    },
    {
        "name": "Notifications",
        "description": (
            "Authenticated user notification endpoints."
        ),
    },
]


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "BusinessOS AI API for authentication, organisations, "
        "invitations, notifications, and platform services."
    ),
    openapi_tags=openapi_tags,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=openapi_tags,
    )

    rate_limit_response = {
        "description": "Too many requests. Rate limit exceeded.",
    }

    for path in schema.get("paths", {}).values():
        for operation in path.values():
            if isinstance(operation, dict) and "responses" in operation:
                operation["responses"].setdefault(
                    "429",
                    rate_limit_response,
                )

    app.openapi_schema = schema

    return app.openapi_schema


app.openapi = custom_openapi


# API rate limiting
app.add_middleware(RateLimitMiddleware)

# Register global exception handlers
register_exception_handlers(app)

# API v1
app.include_router(api_v1_router)


@app.get(
    "/",
    summary="API root",
    description="Return basic information about the BusinessOS AI API.",
)
async def root():
    return {
        "message": "BusinessOS AI API",
        "docs": "/docs",
    }