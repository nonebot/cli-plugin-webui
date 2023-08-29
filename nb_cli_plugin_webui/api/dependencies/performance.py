from nb_cli_plugin_webui.utils.performance import PerformanceMonitor
from nb_cli_plugin_webui.models.schemas.performance import SystemStats


async def get_system_stats() -> SystemStats:
    data = PerformanceMonitor()
    return SystemStats(
        platform=data.get_platform_info(),
        cpu=await data.get_cpu_info(),
        mem=data.get_mem_info(),
        disk=data.get_disk_info(),
        net=data.get_net_info(),
    )
