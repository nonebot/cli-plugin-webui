import re
import sys
import logging
from types import FrameType
from typing import TYPE_CHECKING, Any, cast

import loguru

from nb_cli_plugin_webui.utils import filling_str

if TYPE_CHECKING:
    from loguru import Logger

logger: "Logger" = loguru.logger


class LoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 9
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class LoguruFilter:
    _method_pattern = r'"([A-Z]+)\s.*" (\d{3})'
    _websocket_pattern = r"\('(.+?)', (\d+)\) - \"WebSocket (.+?)\" (\[.+\]|\d+)"

    def _get_color_of_method(self, method: str) -> str:
        if method == "GET":
            return "\033[32m"  # green
        elif method == "POST":
            return "\033[34m"  # blue
        elif method == "PUT":
            return "\033[33m"  # orange
        elif method == "DELETE":
            return "\033[31m"  # red
        elif method == "HEAD":
            return "\033[90m"  # gray
        elif method == "OPTIONS":
            return "\033[93m"  # yellow
        else:
            return "\033[0m"  # default color

    def _get_color_of_code(self, code: str) -> str:
        if code.startswith("2"):
            return "\033[32m"  # green
        elif code.startswith("3"):
            return "\033[33m"  # orange
        elif code.startswith("4"):
            return "\033[31m"  # red
        elif code.startswith("5"):
            return "\033[91m"  # deep red
        else:
            return "\033[0m"  # default color

    def __call__(self, record) -> Any:
        record["name"] = record["name"].split(".")[0]

        message: str = record["message"]
        _match = re.search(self._method_pattern, message)
        if _match:
            request_method = _match.group(1)
            status_code = _match.group(2)

            message = message.replace(f"{request_method} ", str()).replace(
                status_code, str()
            )

            request_method_color = self._get_color_of_method(request_method)
            status_code_color = self._get_color_of_code(status_code)

            new_request_method = request_method_color + filling_str(request_method, 7)
            new_status_code = status_code_color + status_code
            message = (
                f"{new_request_method}\033[0m | {new_status_code}\033[0m | " + message
            )
        else:
            _match = re.search(self._websocket_pattern, message)
            if _match:
                ws_host = _match.group(1)
                ws_port = _match.group(2)
                ws_path = _match.group(3)
                ws_stat = _match.group(4)

                status_code_color = self._get_color_of_code(ws_stat)
                new_status_code = status_code_color + ws_stat

                message = (
                    f"CLIENT  | {new_status_code}\033[0m | "
                    f'{ws_host}:{ws_port} - "{ws_path} WebSocket"'
                )

        record["message"] = message

        return record


log_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "{message}"
)

logger.remove()
logger.add(
    sys.stdout,
    level=0,
    diagnose=False,
    format=log_format,
    filter=LoguruFilter(),
)

STDOUT = logger.level("STDOUT", no=logging.INFO)
