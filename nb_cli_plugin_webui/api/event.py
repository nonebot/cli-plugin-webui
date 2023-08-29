from typing import Callable

from fastapi import FastAPI

from nb_cli_plugin_webui.utils.apscheduler import scheduler
from nb_cli_plugin_webui.api.dependencies.process.manager import ProcessManager
from nb_cli_plugin_webui.api.dependencies.store.manage import (
    DRIVER_MANAGER,
    PLUGIN_MANAGER,
    ADAPTER_MANAGER,
)


def add_event_handler(app: FastAPI) -> FastAPI:
    app.add_event_handler("startup", create_start_app_handler())
    app.add_event_handler("shutdown", create_stop_app_handler())
    return app


def create_start_app_handler() -> Callable:
    async def start_app():
        scheduler.start()

        await PLUGIN_MANAGER.load_item()
        await ADAPTER_MANAGER.load_item()
        await DRIVER_MANAGER.load_item()

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app():
        scheduler.shutdown()

        for process_id in ProcessManager.processes:
            process = ProcessManager.get_process(process_id)
            if process and process.process_is_running:
                await process.stop()

    return stop_app
