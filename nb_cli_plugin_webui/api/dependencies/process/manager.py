from typing import Dict

from nb_cli_plugin_webui.exceptions import ProcessAlreadyExist
from nb_cli_plugin_webui.api.dependencies.process.process import CustomProcessor


class ProcessManager:
    processes: Dict[str, CustomProcessor] = dict()

    get_process = processes.get

    @classmethod
    def add_process(cls, process: CustomProcessor, key: str) -> None:
        if key in cls.processes:
            raise ProcessAlreadyExist
        cls.processes[key] = process

    @classmethod
    def remove_process(cls, key: str) -> None:
        process = cls.processes.pop(key)
        process.logs.listeners.clear()
        return
