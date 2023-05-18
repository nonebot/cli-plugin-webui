from pydantic import BaseModel

from nb_cli_plugin_webui.models.app.machine import (
    RunnerCpuInfo,
    RunnerMemInfo,
    RunnerNetInfo,
    RunnerDiskInfo,
    RunnerPlatformInfo,
)


class SystemStats(BaseModel):
    platform: RunnerPlatformInfo
    cpu: RunnerCpuInfo
    mem: RunnerMemInfo
    disk: RunnerDiskInfo
    net: RunnerNetInfo
