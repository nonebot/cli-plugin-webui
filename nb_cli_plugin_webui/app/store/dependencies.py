from typing import List, Union

from nb_cli_plugin_webui.app.constants import ModuleType
from nb_cli_plugin_webui.app.schemas import Driver, Plugin, Adapter, NoneBotProjectMeta
from nb_cli_plugin_webui.app.handlers import (
    driver_store_manager,
    plugin_store_manager,
    adapter_store_manager,
)


def get_store_items(
    module_type: ModuleType, *, is_search: bool
) -> Union[List[Plugin], List[Adapter], List[Driver]]:
    if module_type == ModuleType.plugin:
        return plugin_store_manager.get_item(is_search=is_search)
    elif module_type == ModuleType.adapter:
        return adapter_store_manager.get_item(is_search=is_search)
    elif module_type == ModuleType.driver:
        return driver_store_manager.get_item(is_search=is_search)
    else:
        raise ValueError("Invalid module type")


def search_store_item(
    module_type: ModuleType,
    project_info: NoneBotProjectMeta,
    content: str,
) -> Union[List[Plugin], List[Adapter], List[Driver]]:
    if module_type == ModuleType.plugin:
        plugin_store_manager.search_item(project_info, content=content)
    elif module_type == ModuleType.adapter:
        adapter_store_manager.search_item(project_info, content=content)
    elif module_type == ModuleType.driver:
        driver_store_manager.search_item(project_info, content=content)
    else:
        raise ValueError("Invalid module type")

    return get_store_items(module_type, is_search=True)
