from fastapi import APIRouter

from .module import router as module_router
from .status import router as status_router
from .config import router as setting_router
from .project import router as project_router

router = APIRouter()
router.include_router(project_router)
router.include_router(module_router, prefix="/module")
router.include_router(status_router, prefix="/status")
router.include_router(setting_router, prefix="/config")
