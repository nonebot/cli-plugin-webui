import re
import json
from pathlib import Path
from typing import List, Optional

from nb_cli.handlers import get_default_python

from nb_cli_plugin_webui.app.utils.process import run_python_script

from . import templates


def _findall(pattern, string) -> str:
    matches = re.findall(pattern, string)
    return matches[0] if matches else str()


async def get_nonebot_loaded_plugins(
    config_file: Path, python_path: Optional[str] = None
) -> List[str]:
    if python_path is None:
        python_path = await get_default_python()

    cwd = config_file.parent
    t = templates.get_template("scripts/nonebot/get_nonebot_loaded_plugins.py.jinja")
    raw_content = await run_python_script(
        python_path, await t.render_async(toml_path=config_file), cwd
    )

    return _findall(r"nonebot_plugins:\s*(.*)", raw_content).split(",")


async def get_nonebot_loaded_config(
    cwd: Optional[Path] = None, python_path: Optional[str] = None
):
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/nonebot/get_nonebot_loaded_config.py.jinja")
    raw_content = await run_python_script(python_path, await t.render_async(), cwd)

    return json.loads(_findall(r"nonebot_loaded_config:\s*(.*)", raw_content))


async def get_nonebot_self_config_schema(
    cwd: Optional[Path] = None, python_path: Optional[str] = None
):
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template(
        "scripts/nonebot/get_nonebot_self_config_schema.py.jinja"
    )
    raw_content = await run_python_script(python_path, await t.render_async(), cwd)

    return json.loads(_findall(r"nonebot_self_config_schema:\s*(.*)", raw_content))


async def get_nonebot_plugin_config_schema(
    plugin: str, cwd: Optional[Path] = None, python_path: Optional[str] = None
):
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template(
        "scripts/nonebot/get_nonebot_plugin_config_schema.py.jinja"
    )
    raw_content = await run_python_script(
        python_path, await t.render_async(plugin=plugin), cwd
    )

    return json.loads(_findall(r"nonebot_plugin_config_schema:\s*(.*)", raw_content))


async def get_nonebot_plugin_metadata(
    plugin: str, cwd: Optional[Path] = None, python_path: Optional[str] = None
):
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/nonebot/get_nonebot_plugin_metadata.py.jinja")
    raw_content = await run_python_script(
        python_path, await t.render_async(plugin=plugin), cwd
    )

    return json.loads(_findall(r"nonebot_plugin_metadata:\s*(.*)", raw_content))
