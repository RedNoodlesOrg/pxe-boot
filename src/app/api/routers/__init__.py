from .boot import router as boot
from .healthcheck import router as healthcheck
from .host import router as host
from .profile import router as profile

__all__ = ["profile", "host", "boot", "healthcheck"]
