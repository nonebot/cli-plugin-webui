from nb_cli_plugin_webui.app.exceptions import BadRequest

from .constants import ErrorCode


class PathIsNotExists(BadRequest):
    detail = ErrorCode.PATH_IS_NOT_EXISTS


class PathIsNotDir(BadRequest):
    detail = ErrorCode.PATH_IS_NOT_DIR
