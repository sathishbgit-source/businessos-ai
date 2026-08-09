from __future__ import annotations

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import settings
from app.core.rate_limiter import InMemoryRateLimiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Global API rate-limiting middleware."""

    def __init__(self, app):
        super().__init__(app)

        self.enabled = settings.rate_limit_enabled

        self.rate_limiter = InMemoryRateLimiter(
            max_requests=settings.rate_limit_requests,
            window_seconds=settings.rate_limit_window_seconds,
        )

    async def dispatch(self, request: Request, call_next):
        if not self.enabled:
            return await call_next(request)

        client_host = request.client.host if request.client else "unknown"

        allowed, retry_after = self.rate_limiter.check(client_host)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                },
                headers={
                    "Retry-After": str(retry_after),
                },
            )

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(
            settings.rate_limit_requests
        )

        return response
