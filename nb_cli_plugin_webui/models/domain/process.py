from enum import Enum
from datetime import datetime

from pydantic import Field, BaseModel

from nb_cli_plugin_webui.core.log import STDOUT


class LogLevel(str, Enum):
    STDOUT = STDOUT.name

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class CustomLog(BaseModel):
    time: datetime = Field(
        default_factory=lambda: datetime.now().strftime("%H:%M:%S.%f")[:-3]
    )
    level: str = str()
    message: str


class ProcessLog(CustomLog):
    level: LogLevel = LogLevel.STDOUT
