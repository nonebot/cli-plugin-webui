from nb_cli_plugin_webui.app.exceptions import PermissionDenied

from .constants import ErrorCode


class TokenInvalid(PermissionDenied):
    detail = ErrorCode.TOKEN_INVALID
