from typing import List, Union

from nb_cli_plugin_webui.app.models.store import Plugin
from nb_cli_plugin_webui.app.models.types import ModuleType
from nb_cli_plugin_webui.app.models.base import Driver, Adapter, NoneBotProjectMeta
from nb_cli_plugin_webui.app.handlers import (
    driver_store_manager,
    plugin_store_manager,
    adapter_store_manager,
)


def get_store_items(
    module_type: ModuleType, *, is_search: bool
) -> Union[List[Plugin], List[Adapter], List[Driver]]:
    if module_type == ModuleType.PLUGIN:
        return plugin_store_manager.get_item(is_search=is_search)
    elif module_type == ModuleType.ADAPTER:
        return adapter_store_manager.get_item(is_search=is_search)
    elif module_type == ModuleType.DRIVER:
        return driver_store_manager.get_item(is_search=is_search)
    else:
        raise ValueError("Invalid module type")


def search_store_item(
    module_type: ModuleType,
    project_info: NoneBotProjectMeta,
    content: str,
) -> Union[List[Plugin], List[Adapter], List[Driver]]:
    if module_type == ModuleType.PLUGIN:
        plugin_store_manager.search_item(project_info, content=content)
    elif module_type == ModuleType.ADAPTER:
        adapter_store_manager.search_item(project_info, content=content)
    elif module_type == ModuleType.DRIVER:
        driver_store_manager.search_item(project_info, content=content)
    else:
        raise ValueError("Invalid module type")

    return get_store_items(module_type, is_search=True)
