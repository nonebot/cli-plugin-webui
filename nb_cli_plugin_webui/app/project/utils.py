from pathlib import Path

import tomlkit
from nb_cli.config.parser import CONFIG_FILE, CONFIG_FILE_ENCODING

from .schemas import ProjectTomlDetail


def get_nonebot_info_from_toml(working_dir: Path) -> ProjectTomlDetail:
    path = working_dir / CONFIG_FILE
    if not path.is_file():
        raise FileNotFoundError
    data = tomlkit.loads(path.read_text(encoding=CONFIG_FILE_ENCODING))

    project_name = data.get("project", dict()).get("name", str())
    tool_detail = data.get("tool", dict())

    nonebot_info = tool_detail.get("nonebot", dict())
    adapters = nonebot_info.get("adapters", list())
    plugins = nonebot_info.get("plugins", list())
    plugin_dirs = nonebot_info.get("plugin_dirs", list())

    # TODO
    builtin_plugins = list()

    return ProjectTomlDetail(
        project_name=project_name,
        adapters=adapters,
        plugins=plugins,
        plugin_dirs=plugin_dirs,
        builtin_plugins=builtin_plugins,
    )
