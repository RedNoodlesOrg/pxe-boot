from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROFILES: Path = Path("./profiles")
    ARTIFACTS: Path = Path("./artifacts")
    PXE_BASE_URL: str = "http://pxe.lab/fcos"
    COREOS_VERSION: str = "40.20240901.3.0"
    STREAM: str = "stable"
    DB_URL: str = "sqlite+aiosqlite:///./app.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
settings.PROFILES.mkdir(parents=True, exist_ok=True)
settings.ARTIFACTS.mkdir(parents=True, exist_ok=True)
