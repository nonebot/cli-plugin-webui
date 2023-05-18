from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from nb_cli_plugin_webui.config import config
from nb_cli_plugin_webui.exceptions import ConfigIsNotExist
from nb_cli_plugin_webui.api.routes.api import router as api_router
from nb_cli_plugin_webui.api.event import (
    create_stop_app_handler,
    create_start_app_handler,
)


def get_application() -> FastAPI:
    if not config.exist:
        raise ConfigIsNotExist

    conf = config.read()
    app = FastAPI(**conf.server.fastapi_kwargs)
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=...,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", create_start_app_handler)
    app.add_event_handler("shutdown", create_stop_app_handler)

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()
