from fastapi import APIRouter

from nb_cli_plugin_webui.api.routes import performance, authentication

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(performance.router, tags=["performance"], prefix="/performance")
