from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routers import boot, host, profile
from .core.db import engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(
    title="PXE Ignition Service",
    version="1.0.0",
    lifespan=lifespan,
)

# Routers
app.include_router(profile)
app.include_router(host)
app.include_router(boot)
