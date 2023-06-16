from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.api.event import add_event_handler
from nb_cli_plugin_webui.exceptions import ConfigIsNotExist
from nb_cli_plugin_webui.api.error import add_exception_handler
from nb_cli_plugin_webui.api.routes.api import router as api_router
from nb_cli_plugin_webui.api.dependencies.authentication import CustomAuthMiddleware


def get_application() -> FastAPI:
    if not config.exist:
        raise ConfigIsNotExist

    conf = config.read()
    app = FastAPI(**conf.server.fastapi_kwargs)
    app.add_middleware(CustomAuthMiddleware, pass_paths=["/api/auth"])
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

    return app


app = get_application()
