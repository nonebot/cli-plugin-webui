from typing import Union

from nb_cli_plugin_webui.app.schemas import Driver, Plugin, Adapter
from nb_cli_plugin_webui.app.handlers import (
    ModuleStoreManager,
    driver_store_manager,
    plugin_store_manager,
    adapter_store_manager,
)

from .exception import ModuleTypeNotFound


def get_store_manager(
    module_type: str,
) -> Union[
    ModuleStoreManager[Plugin], ModuleStoreManager[Adapter], ModuleStoreManager[Driver]
]:
    if module_type == "plugin":
        return plugin_store_manager
    elif module_type == "adapter":
        return adapter_store_manager
    elif module_type == "driver":
        return driver_store_manager
    else:
        raise ModuleTypeNotFound()
