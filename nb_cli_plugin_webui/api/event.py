from typing import Callable

from fastapi import FastAPI

from nb_cli_plugin_webui.utils.apscheduler import scheduler


def add_event_handler(app: FastAPI) -> FastAPI:
    app.add_event_handler("startup", create_start_app_handler)
    app.add_event_handler("shutdown", create_stop_app_handler)
    return app


def create_start_app_handler() -> Callable:
    async def start_app():
        scheduler.start()

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app():
        scheduler.shutdown()

    return stop_app
