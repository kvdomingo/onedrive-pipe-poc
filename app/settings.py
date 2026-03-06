from pathlib import Path

from anyio.functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    WEBHOOK_SECRET: SecretStr
    NGROK_AUTHTOKEN: SecretStr


@lru_cache
def _get_settings() -> Settings:
    return Settings()  # ty:ignore[missing-argument]


settings = _get_settings()
