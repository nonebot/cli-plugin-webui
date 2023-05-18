from typing import Callable

from nb_cli_plugin_webui.utils.apscheduler import scheduler


def create_start_app_handler() -> Callable:
    async def start_app():
        scheduler.start()

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app():
        scheduler.shutdown()

    return stop_app
