import platform
from sys import platform as pf

import psutil
import pythoncom

from nb_cli_plugin_webui.utils.apscheduler import scheduler
from nb_cli_plugin_webui.models.app.machine import (
    RunnerCpuInfo,
    RunnerMemInfo,
    RunnerNetInfo,
    RunnerDiskInfo,
    RunnerPlatformInfo,
)

if pf == "win32":
    import wmi
    from win32com import client


_last_net_io = [0, 0]
_now_net_io = [0, 0]


@scheduler.scheduled_job("interval", seconds=1, misfire_grace_time=15)
async def _():
    global _last_net_io, _now_net_io

    net_counters = psutil.net_io_counters()
    _now_net_io = [
        net_counters.bytes_sent - _last_net_io[0],
        net_counters.bytes_recv - _last_net_io[1],
    ]
    _last_net_io = [net_counters.bytes_sent, net_counters.bytes_recv]


class PlatformPerformanceMonitor:
    """获取当前运行平台性能信息"""

    @staticmethod
    def get_platform_info() -> RunnerPlatformInfo:
        return RunnerPlatformInfo(
            name=platform.platform(),
            struct=platform.architecture()[0],
            platform_type=pf,
        )

    @staticmethod
    def get_cpu_info() -> RunnerCpuInfo:
        cpu_name = platform.processor()
        if pf == "win32":
            pythoncom.CoInitialize()
            winm = client.GetObject("winmgmts:root\cimv2")
            cpus = winm.ExecQuery("SELECT * FROM Win32_Processor")
            cpu_name = cpus[0].Name.strip()

        cpu_cores = psutil.cpu_count(False)
        _freq = psutil.cpu_freq()
        cpu_max_freq = f"{'%.2f'%(_freq.max / 1000)}"
        cpu_current_freq = f"{'%.2f'%(_freq.current / 1000)}"
        cpu_percent = psutil.cpu_percent(interval=0.1)
        process = len(psutil.pids())

        return RunnerCpuInfo(
            name=cpu_name,
            count=cpu_cores,
            max_freq=cpu_max_freq,
            current_freq=cpu_current_freq,
            percent=cpu_percent,
            process=process,
        )

    @staticmethod
    def get_mem_info() -> RunnerMemInfo:
        vm = psutil.virtual_memory()

        return RunnerMemInfo(
            total=vm.total,
            available=vm.available,
            percent=vm.percent,
            used=vm.used,
            free=vm.free,
        )

    @staticmethod
    def get_disk_info() -> RunnerDiskInfo:
        disk_total = int()
        disk_used = int()
        disk_free = int()
        if pf == "win32":
            pythoncom.CoInitialize()
            w = wmi.WMI()
            disk_list = [d.DeviceID for d in w.Win32_LogicalDisk()]
            for i in disk_list:
                disk = psutil.disk_usage(i)
                disk_total += disk.total
                disk_used += disk.used
                disk_free += disk.free
        else:
            disk = psutil.disk_usage("/")
            disk_total = disk.total
            disk_used = disk.used
            disk_free = disk.free

        return RunnerDiskInfo(total=disk_total, used=disk_used, free=disk_free)

    @staticmethod
    def get_net_info() -> RunnerNetInfo:
        net = psutil.net_io_counters()
        return RunnerNetInfo(
            sent_total=net.bytes_sent,
            recv_total=net.bytes_recv,
            package_sent=net.packets_sent,
            package_recv=net.packets_recv,
            speed=_now_net_io,
        )
