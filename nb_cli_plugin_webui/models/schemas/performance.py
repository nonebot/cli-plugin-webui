from typing import List

from pydantic import BaseModel


class PlatformInfo(BaseModel):
    name: str
    struct: str
    platform_type: str


class CpuInfo(BaseModel):
    name: str
    count: int
    max_freq: str
    current_freq: str
    percent: float
    process: int


class MemInfo(BaseModel):
    total: int
    available: int
    percent: float
    used: int
    free: int


class DiskInfo(BaseModel):
    total: int
    used: int
    free: int
    speed: List[int]


class NetInfo(BaseModel):
    sent_total: int
    recv_total: int
    package_sent: int
    package_recv: int
    speed: List[int]


class SystemStats(BaseModel):
    platform: PlatformInfo
    cpu: CpuInfo
    mem: MemInfo
    disk: DiskInfo
    net: NetInfo


class SystemStatsResponse(BaseModel):
    system_stats: SystemStats
