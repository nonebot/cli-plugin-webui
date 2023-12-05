from typing import List, Union, Literal

from nb_cli_plugin_webui.app.schemas import Driver
from nb_cli_plugin_webui.app.schemas import Adapter
from nb_cli_plugin_webui.app.schemas import GenericResponse
from nb_cli_plugin_webui.app.schemas import Plugin as BasePlugin
from nb_cli_plugin_webui.app.schemas import ModuleInfo as BaseModuleInfo


class Plugin(BasePlugin):
    module_type: Literal["plugin"]


class ModuleInfo(BaseModuleInfo):
    module_type: Literal["module"]


class StoreListResponse(
    GenericResponse[Union[List[BasePlugin], List[Adapter], List[Driver]]]
):
    now_page: int
    total_page: int
    total_item: int
