import platform
from sys import platform as pf

import psutil

from nb_cli_plugin_webui.models.schemas.machine import *

if pf == "win32":
    import wmi
    from win32com.client import GetObject


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
            winm = GetObject("winmgmts:root\cimv2")
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
        ...
