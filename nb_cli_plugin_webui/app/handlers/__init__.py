from pathlib import Path

from jinja2 import Environment, FileSystemLoader

templates = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=False,
    enable_async=True,
    loader=FileSystemLoader(Path(__file__).parent.parent / "template"),
)

# flake8:noqa:f402
from .pip import call_pip, call_pip_install
from .project import NoneBotProjectList, NoneBotProjectManager
from .store import (
    ModuleStoreManager,
    load_module_data,
    driver_store_manager,
    plugin_store_manager,
    adapter_store_manager,
)
from .nonebot import (
    get_nonebot_loaded_config,
    get_nonebot_loaded_plugins,
    get_nonebot_plugin_metadata,
    get_nonebot_self_config_schema,
    get_nonebot_plugin_config_schema,
)
