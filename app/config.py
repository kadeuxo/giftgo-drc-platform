"""Application configuration and constants."""
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = Field("GiftGo API", description="Public name of the API")
    database_url: str = Field(
        default_factory=lambda: f"sqlite:///{Path(__file__).resolve().parent.parent / 'giftgo.db'}",
        description="Database connection string",
    )
    allow_origins: list[str] = Field(
        default_factory=lambda: ["*"],
        description="List of origins allowed to access the API",
    )

    @validator("allow_origins", pre=True)
    def _split_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    class Config:
        env_prefix = "GIFTGO_"
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
