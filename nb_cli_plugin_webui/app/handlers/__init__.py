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
from .nonebot import get_nonebot_config_detail
from .project import NoneBotProjectList, NoneBotProjectManager
from .plugin import get_nonebot_plugin_list, get_nonebot_plugin_config_detail
from .store import (
    ModuleStoreManager,
    load_module_data,
    driver_store_manager,
    plugin_store_manager,
    adapter_store_manager,
)
