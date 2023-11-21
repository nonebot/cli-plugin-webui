from typing import List, Optional

from pydantic import BaseModel

from nb_cli_plugin_webui.app.handlers.process import ProcessInfo


class PlatformProfile(BaseModel):
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


class SystemInfo(BaseModel):
    platform: PlatformProfile
    cpu: CpuInfo
    mem: MemInfo
    disk: DiskInfo
    net: NetInfo


class StatusInfo(BaseModel):
    system: SystemInfo
    process: Optional[ProcessInfo]
