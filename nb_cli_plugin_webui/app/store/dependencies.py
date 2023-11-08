from typing import List, Union, Literal

from nb_cli_plugin_webui.app.schemas import Driver, Plugin, Adapter, NoneBotProjectMeta
from nb_cli_plugin_webui.app.handlers import (
    driver_store_manager,
    plugin_store_manager,
    adapter_store_manager,
)

ASSIGN_MODULE_TYPE = Literal["plugin", "adapter", "driver"]


def get_store_items(
    module_type: ASSIGN_MODULE_TYPE, *, is_search: bool
) -> Union[List[Plugin], List[Adapter], List[Driver]]:
    if module_type == "plugin":
        return plugin_store_manager.get_item(is_search=is_search)
    elif module_type == "adapter":
        return adapter_store_manager.get_item(is_search=is_search)
    elif module_type == "driver":
        return driver_store_manager.get_item(is_search=is_search)
    else:
        raise ValueError("Invalid module type")


def search_store_item(
    module_type: ASSIGN_MODULE_TYPE,
    project_info: NoneBotProjectMeta,
    content: str,
) -> Union[List[Plugin], List[Adapter], List[Driver]]:
    if module_type == "plugin":
        plugin_store_manager.search_item(project_info, content=content)
    elif module_type == "adapter":
        adapter_store_manager.search_item(project_info, content=content)
    elif module_type == "driver":
        driver_store_manager.search_item(project_info, content=content)
    else:
        raise ValueError("Invalid module type")

    return get_store_items(module_type, is_search=True)
