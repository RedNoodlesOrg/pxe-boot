from .boot import router as boot
from .host import router as host
from .profile import router as profile
from .healthcheck import router as healthcheck
__all__ = ["profile", "host", "boot", "healthcheck"]
