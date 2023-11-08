from pathlib import Path

import tomlkit

from .schemas import ProjectTomlDetail


def get_nonebot_info_from_toml(working_dir: Path) -> ProjectTomlDetail:
    path = working_dir / "pyproject.toml"
    if not path.is_file():
        raise FileNotFoundError
    data = tomlkit.loads(path.read_text(encoding="utf-8"))

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
