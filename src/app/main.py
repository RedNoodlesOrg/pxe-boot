from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routers import boot, healthcheck, host, profile
from .core.db import engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(
    title="PXE Ignition Service",
    version="0.1.0",
    lifespan=lifespan,
)

# Routers
app.include_router(profile)
app.include_router(host)
app.include_router(boot)
app.include_router(healthcheck)
