from typing import List
from pydantic import BaseModel


class RunnerPlatformInfo(BaseModel):
    name: str
    struct: str
    platform_type: str


class RunnerCpuInfo(BaseModel):
    name: str
    count: int
    max_freq: str
    current_freq: str
    percent: float
    process: int


class RunnerMemInfo(BaseModel):
    total: int
    available: int
    percent: float
    used: int
    free: int


class RunnerDiskInfo(BaseModel):
    total: int
    used: int
    free: int


class RunnerNetInfo(BaseModel):
    sent_total: int
    recv_total: int
    package_sent: int
    package_recv: int
    speed: List[int]

