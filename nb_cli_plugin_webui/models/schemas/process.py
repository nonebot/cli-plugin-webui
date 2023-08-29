from typing import Optional

from pydantic import BaseModel


class ProcessPerformance(BaseModel):
    cpu: float
    mem: float


class ProcessInfo(BaseModel):
    status_code: Optional[int]
    total_log: int
    is_running: bool
    performance: Optional[ProcessPerformance]
