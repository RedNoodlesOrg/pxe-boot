# tests/conftest.py
import os
import shutil
import tempfile
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


@pytest.fixture(scope="session")
def temp_env():
    root = Path(tempfile.mkdtemp(prefix="pxeign-"))
    profiles = root / "profiles"
    profiles.mkdir(parents=True, exist_ok=True)
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    db_path = root / "test.db"

    os.environ["PROFILES_DIR"] = str(profiles)
    os.environ["ARTIFACTS_DIR"] = str(artifacts)
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path}"

    yield {"root": root, "profiles": profiles, "artifacts": artifacts, "db": db_path}
    shutil.rmtree(root, ignore_errors=True)


@pytest.fixture(scope="session", autouse=True)
def _bind_settings(temp_env):
    from app.core import config as cfg
    from app.core import db as dbmod

    cfg.settings.profiles_dir = temp_env["profiles"]
    cfg.settings.artifacts_dir = temp_env["artifacts"]
    cfg.settings.database_url = f"sqlite+aiosqlite:///{temp_env['db']}"

    dbmod.engine = create_async_engine(
        cfg.settings.database_url, echo=False, future=True
    )
    dbmod.SessionLocal = async_sessionmaker(
        dbmod.engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest_asyncio.fixture(scope="session")
async def app_instance():
    from app.main import app

    return app
