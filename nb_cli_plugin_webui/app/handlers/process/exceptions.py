from nb_cli_plugin_webui.app.exceptions import NotFound, BadRequest

from .constants import ErrorCode


class ProcessAlreadyExists(BadRequest):
    detail = ErrorCode.PROCESS_ALREADY_EXISTS


class ProcessAlreadyRunning(BadRequest):
    detail = ErrorCode.PROCESS_ALREADY_RUNNING


class ProcessNotFound(NotFound):
    detail = ErrorCode.NOT_FOUND_PROCESS


class LogStorageNotFound(NotFound):
    detail = ErrorCode.NOT_FOUND_LOG_STORAGE


class LogStorageAlreadyExists(BadRequest):
    detail = ErrorCode.LOG_STORAGE_EXISTS
