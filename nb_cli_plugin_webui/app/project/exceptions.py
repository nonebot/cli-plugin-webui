from nb_cli_plugin_webui.app.exceptions import NotFound, BadRequest

from .constants import ErrorCode


class NoneBotProjectNotFound(NotFound):
    detail = ErrorCode.PROJECT_NOT_FOUND


class ProjectDirIsNotDir(BadRequest):
    detail = ErrorCode.PROJECT_DIR_NOT_DIR


class ProjectDeleteFailed(BadRequest):
    detail = ErrorCode.PROJECT_DELETE_FAILED


class WriteNoneBotProjectProfileFailed(BadRequest):
    detail = ErrorCode.PROJECT_WRITE_PROFILE_FAILED


class ProjectTomlNotFound(BadRequest):
    detail = ErrorCode.PROJECT_TOML_NOT_FOUND
