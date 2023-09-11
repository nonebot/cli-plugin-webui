import asyncio
import platform
from sys import platform as pf

import psutil

from nb_cli_plugin_webui.utils.apscheduler import scheduler
from nb_cli_plugin_webui.models.schemas.performance import (
    CpuInfo,
    MemInfo,
    NetInfo,
    DiskInfo,
    PlatformInfo,
)

if pf == "win32":
    import wmi  # type: ignore
    import pythoncom
    from win32com import client


_LAST_DISK_IO = [0, 0]
_NOW_DISK_IO = [0, 0]
_LAST_NET_IO = [0, 0]
_NOW_NET_IO = [0, 0]


@scheduler.scheduled_job("interval", seconds=1, misfire_grace_time=15)
async def get_disk_io():
    global _LAST_DISK_IO, _NOW_DISK_IO

    disk_counters = psutil.disk_io_counters()
    if disk_counters is None:
        return

    _NOW_DISK_IO = [
        disk_counters.read_bytes - _LAST_DISK_IO[0],
        disk_counters.write_bytes - _LAST_DISK_IO[1],
    ]
    _LAST_DISK_IO = [disk_counters.read_bytes, disk_counters.write_bytes]


@scheduler.scheduled_job("interval", seconds=1, misfire_grace_time=15)
async def get_net_io():
    global _LAST_NET_IO, _NOW_NET_IO

    net_counters = psutil.net_io_counters()
    _NOW_NET_IO = [
        net_counters.bytes_sent - _LAST_NET_IO[0],
        net_counters.bytes_recv - _LAST_NET_IO[1],
    ]
    _LAST_NET_IO = [net_counters.bytes_sent, net_counters.bytes_recv]


class PerformanceMonitor:
    """获取当前运行平台性能信息"""

    @staticmethod
    def get_platform_info() -> PlatformInfo:
        return PlatformInfo(
            name=platform.platform(),
            struct=platform.architecture()[0],
            platform_type=pf,
        )

    @staticmethod
    async def get_cpu_info() -> CpuInfo:
        cpu_name = platform.processor()
        if pf == "win32":
            pythoncom.CoInitialize()
            winm = client.GetObject("winmgmts:root\cimv2")
            cpus = winm.ExecQuery("SELECT * FROM Win32_Processor")
            cpu_name = cpus[0].Name.strip()

        cpu_cores = psutil.cpu_count(False)
        _freq = int()
        cpu_max_freq = "0"
        cpu_current_freq = "0"
        if pf != "darwin":
            _freq = psutil.cpu_freq()
            cpu_max_freq = f"{'%.2f'%(_freq.max / 1000)}"
            cpu_current_freq = f"{'%.2f'%(_freq.current / 1000)}"

        psutil.cpu_percent(percpu=True)
        await asyncio.sleep(0.5)
        raw_cpu_percent = psutil.cpu_percent(percpu=True)
        cpu_percent = sum(raw_cpu_percent) / len(raw_cpu_percent)

        process = len(psutil.pids())

        return CpuInfo(
            name=cpu_name,
            count=cpu_cores,
            max_freq=cpu_max_freq,
            current_freq=cpu_current_freq,
            percent=cpu_percent,
            process=process,
        )

    @staticmethod
    def get_mem_info() -> MemInfo:
        vm = psutil.virtual_memory()

        return MemInfo(
            total=vm.total,
            available=vm.available,
            percent=vm.percent,
            used=vm.used,
            free=vm.free,
        )

    @staticmethod
    def get_disk_info() -> DiskInfo:
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

        return DiskInfo(
            total=disk_total, used=disk_used, free=disk_free, speed=_NOW_DISK_IO
        )

    @staticmethod
    def get_net_info() -> NetInfo:
        net = psutil.net_io_counters()
        return NetInfo(
            sent_total=net.bytes_sent,
            recv_total=net.bytes_recv,
            package_sent=net.packets_sent,
            package_recv=net.packets_recv,
            speed=_NOW_NET_IO,
        )
