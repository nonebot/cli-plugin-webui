from pydantic import BaseModel

from nb_cli_plugin_webui.models.app.performance import SystemStats


class SystemStatsResponse(BaseModel):
    system_stats: SystemStats
