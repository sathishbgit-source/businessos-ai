from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    app_name: str = "BusinessOS AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    database_url: str
    database_echo: bool = False

    # ------------------------------------------------------------------
    # JWT Authentication
    # ------------------------------------------------------------------
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

        # ------------------------------------------------------------------
    # API Rate Limiting
    # ------------------------------------------------------------------
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    # ------------------------------------------------------------------
    # Future Infrastructure
    # ------------------------------------------------------------------
    redis_url: str | None = None

    openai_api_key: str | None = None

    log_level: str = "INFO"

    # ------------------------------------------------------------------
    # Pydantic Settings
    # ------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    The settings object is created only once during the application's
    lifetime and reused everywhere.
    """
    return Settings()


settings = get_settings()