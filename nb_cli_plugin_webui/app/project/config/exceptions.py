from nb_cli_plugin_webui.app.exceptions import NotFound, BadRequest, BaseServerException

from .constants import ErrorCode


class EnvExists(BadRequest):
    detail = ErrorCode.ENV_EXISTS


class EnvNotFound(NotFound):
    detail = ErrorCode.ENV_NOT_FOUND


class ConfigNotFound(NotFound):
    detail = ErrorCode.CONFIG_NOT_FOUND


class BaseEnvCannotBeDeleted(BadRequest):
    detail = ErrorCode.BASE_ENV_CANNOT_BE_DELETED


class ConfigParseError(BadRequest):
    detail = ErrorCode.CONFIG_PARSE_ERROR


class GetConfigError(BaseServerException):
    detail = ErrorCode.GET_CONFIG_ERROR
