from pathlib import Path

from starlette.types import Scope
from starlette.responses import Response
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarlettleHTTPException

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.api.event import add_event_handler
from nb_cli_plugin_webui.exceptions import ConfigIsNotExist
from nb_cli_plugin_webui.api.error import add_exception_handler
from nb_cli_plugin_webui.api.routes.api import router as api_router
from nb_cli_plugin_webui.api.dependencies.authentication import CustomAuthMiddleware

DIST_PATH = Path(__file__).parent.parent / "dist"

if not DIST_PATH.is_dir():
    raise FileNotFoundError(_("WebUI dist directory not found."))


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarlettleHTTPException) as err:
            if err.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise err


def init_application() -> FastAPI:
    if not config.exist:
        raise ConfigIsNotExist

    conf = config.read()
    app = FastAPI(**conf.fastapi_kwargs)
    app.add_middleware(
        CustomAuthMiddleware,
        auth_router=["/api"],
        pass_paths=["/api/auth/login"],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app = add_event_handler(app)
    app = add_exception_handler(app)

    app.include_router(api_router, prefix="/api")

    app.mount("/", SPAStaticFiles(directory=DIST_PATH, html=True), "NoneBot WebUI")

    return app


app = init_application()
