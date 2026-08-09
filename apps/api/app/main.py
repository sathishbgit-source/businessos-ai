from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
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

# API v1
app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {
        "message": "BusinessOS AI API",
        "docs": "/docs",
    }
