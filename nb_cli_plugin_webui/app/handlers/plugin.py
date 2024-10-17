import json
import asyncio
from pathlib import Path
from typing import List, Optional

from nb_cli.handlers.process import create_process
from nb_cli.handlers.meta import get_default_python

from nb_cli_plugin_webui.app.utils.process import run_python_script

from . import templates


async def get_nonebot_plugin_list(
    config_file: Path, python_path: Optional[str] = None
) -> List[str]:
    if python_path is None:
        python_path = await get_default_python()

    cwd = config_file.parent
    t = templates.get_template("scripts/plugin/get_loaded_plugins.py.jinja")
    raw_content = await run_python_script(
        python_path, await t.render_async(toml_path=config_file), cwd
    )
    return raw_content.split(",")


async def get_nonebot_plugin_config_detail(
    plugin: str, python_path: Optional[str] = None
) -> dict:
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/plugin/get_plugin_config_detail.py.jinja")
    raw_content = await run_python_script(
        python_path, await t.render_async(plugin=plugin)
    )
    config_schema = dict()
    if raw_content and raw_content != "Failed":
        parsed_stdout = json.loads(raw_content)

        config_schema = parsed_stdout["schema"]
        config_set = parsed_stdout["config"]

        for i in config_set:
            config_schema["properties"][i]["configured"] = config_set[i]
            config_schema["properties"][i]["latest_change"] = ".env"

    return config_schema


async def get_nonebot_plugin_detail(
    plugin: str, python_path: Optional[str] = None
) -> dict:
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/plugin/get_plugin_metadata.py.jinja")
    proc = await create_process(
        python_path,
        "-c",
        await t.render_async(plugin=plugin),
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    raw_content = stdout.decode().strip()
    plugin_info = dict()
    if raw_content:
        plugin_info = json.loads(raw_content)

    return plugin_info
