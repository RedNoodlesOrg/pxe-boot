
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.db import init_db, engine
from .api.routers import host, profile, boot

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
