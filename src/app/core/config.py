from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    profiles_dir: Path = Path("./profiles")
    artifacts_dir: Path = Path("./artifacts")
    pxe_base_url: str = "http://pxe.lab/fcos"
    ignition_base_url: str = "http://localhost:8000"
    fcos_version: str = "40.20240901.3.0"

    database_url: str = "sqlite+aiosqlite:///./app.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
settings.profiles_dir.mkdir(parents=True, exist_ok=True)
settings.artifacts_dir.mkdir(parents=True, exist_ok=True)