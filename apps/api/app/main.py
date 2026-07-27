from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "message": "BusinessOS AI API",
        "docs": "/docs",
    }
