from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.invitations import (
    router as invitation_router,
)
from app.api.v1.organisations import (
    router as organisation_router,
)
from app.config import settings
from app.core.exception_handlers import (
    register_exception_handlers,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# Register global exception handlers
register_exception_handlers(app)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(organisation_router)
app.include_router(invitation_router)

@app.get("/")
async def root():
    return {
        "message": "BusinessOS AI API",
        "docs": "/docs",
    }