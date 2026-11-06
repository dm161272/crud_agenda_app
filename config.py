from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = "dev"
    app_name: str = "crud_agenda_app"
    debug: bool = False

    database_url: str = "sqlite:///crud_agenda_app.db"
    secret_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None

    # only for Reflex itself
    api_url: str = "http://localhost:8000"


    @model_validator(mode="after")
    def _require_key_in_prod(self):
        if self.env == "prod" and self.secret_key is None:
            raise ValueError("SECRET_KEY is required in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
