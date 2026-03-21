from fastapi import APIRouter

from .agents import router as agents_router
from .dashboard import router as dashboard_router
from .discovery import router as discovery_router
from .health import router as health_router
from .mcps import router as mcps_router
from .skills import router as skills_router
from .workflows import router as workflows_router


def build_api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health_router)
    router.include_router(dashboard_router)
    router.include_router(discovery_router)
    router.include_router(skills_router)
    router.include_router(mcps_router)
    router.include_router(agents_router)
    router.include_router(workflows_router)
    return router
