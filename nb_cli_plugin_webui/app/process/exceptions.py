from nb_cli_plugin_webui.app.exceptions import NotFound

from .constants import ErrorCode


class AdapterNotFound(NotFound):
    detail = ErrorCode.NOT_FOUND_ADAPTER


class DriverNotFound(NotFound):
    detail = ErrorCode.NOT_FOUND_DRIVER
