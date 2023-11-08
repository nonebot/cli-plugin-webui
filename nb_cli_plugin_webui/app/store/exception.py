from nb_cli_plugin_webui.app.exceptions import NotFound

from .constants import ErrorCode


class ModuleTypeNotFound(NotFound):
    detail = ErrorCode.MODULE_TYPE_NOT_FOUND
