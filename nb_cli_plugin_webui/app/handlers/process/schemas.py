from enum import Enum
from datetime import datetime
from typing import Union, Optional

from pydantic import Field, BaseModel


class LogLevel(str, Enum):
    STDOUT = "STDOUT"

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class CustomLog(BaseModel):
    time: Union[datetime, str] = Field(
        default_factory=lambda: datetime.now().strftime("%H:%M:%S.%f")[:-3]
    )
    level: str = str()
    message: str


class ProcessLog(CustomLog):
    level: LogLevel = LogLevel.STDOUT


class ProcessPerformance(BaseModel):
    cpu: float
    mem: float


class ProcessInfo(BaseModel):
    status_code: Optional[int]
    total_log: int
    is_running: bool
    performance: Optional[ProcessPerformance]
