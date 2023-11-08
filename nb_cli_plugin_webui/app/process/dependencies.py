from nb_cli_plugin_webui.app.handlers.process import (
    Processor,
    LogStorage,
    ProcessManager,
    ProcessNotFound,
    LogStorageFather,
    LogStorageNotFound,
)


def get_process(project_id: str) -> Processor:
    process = ProcessManager.get_process(project_id)
    if process is None:
        raise ProcessNotFound()
    return process


def get_log_storage(log_id: str) -> LogStorage:
    log_storage = LogStorageFather.get_storage(log_id)
    if log_storage is None:
        raise LogStorageNotFound()
    return log_storage
