from nb_cli_plugin_webui.models.app.performance import SystemStats
from nb_cli_plugin_webui.utils.performance import PlatformPerformanceMonitor


def get_system_stats() -> SystemStats:
    data = PlatformPerformanceMonitor()
    return SystemStats(
        platform=data.get_platform_info(),
        cpu=data.get_cpu_info(),
        mem=data.get_mem_info(),
        disk=data.get_disk_info(),
        net=data.get_net_info(),
    )
