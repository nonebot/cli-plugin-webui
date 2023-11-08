from nb_cli_plugin_webui.app.exceptions import NotFound, BadRequest

from .constants import ErrorCode


class EnvExists(BadRequest):
    detail = ErrorCode.ENV_EXISTS


class EnvNotFound(NotFound):
    detail = ErrorCode.ENV_NOT_FOUND


class ConfigNotFound(NotFound):
    detail = ErrorCode.CONFIG_NOT_FOUND
