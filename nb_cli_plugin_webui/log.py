import sys
import logging
from types import FrameType
from typing import TYPE_CHECKING, cast

import loguru

if TYPE_CHECKING:
    from loguru import Logger

logger: "Logger" = loguru.logger


class LoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


log_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "{message}"
)

logger.remove()
logger_id = logger.add(
    sys.stdout,
    level=0,
    diagnose=False,
    format=log_format,
)
