from fastapi import APIRouter

from src.api.routes.system import router as system_router
from src.api.routes.targets import router as targets_router


def build_api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(system_router)
    router.include_router(targets_router)
    return router
