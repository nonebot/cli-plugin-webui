from fastapi import APIRouter

from nb_cli_plugin_webui.api.routes.project import api as project
from nb_cli_plugin_webui.api.routes import (
    log,
    check,
    files,
    store,
    performance,
    authentication,
)

router = APIRouter()
router.include_router(authentication.router, prefix="/auth")
router.include_router(performance.router, prefix="/performance")
router.include_router(project.router, prefix="/project")
router.include_router(check.router, prefix="/check")
router.include_router(files.router, prefix="/file")
router.include_router(store.router, prefix="/store")
router.include_router(log.router, prefix="/log")
