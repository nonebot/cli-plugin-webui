import sys
import json
import asyncio
from typing import Optional

from nb_cli.handlers.process import create_process
from nb_cli.handlers.meta import get_default_python

from nb_cli_plugin_webui.api.dependencies import templates


async def get_plugin_list(python_path: Optional[str] = None) -> list:
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/script/list_assign_prefix_pkg.py.jinja")
    if sys.version_info >= (3, 10):
        temp = await t.render_async(pkg_prefix="nonebot_plugin")
    else:
        temp = await t.render_async(pkg_prefix="nonebot-plugin")
    proc = await create_process(
        python_path,
        "-c",
        temp,
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    raw_content = stdout.decode().strip()
    result = list()
    if raw_content:
        result = raw_content.split(",")
        result = [plugin.replace("-", "_") for plugin in result]

    return result


async def get_plugin_config_detail(
    plugin: str, python_path: Optional[str] = None
) -> dict:
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/plugin/get_plugin_config_detail.py.jinja")
    proc = await create_process(
        python_path,
        "-c",
        await t.render_async(plugin_name=plugin),
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    raw_content = stdout.decode().strip()
    config_schema = dict()
    if raw_content and raw_content != "Failed":
        parsed_stdout = json.loads(stdout.decode().strip())

        config_schema = parsed_stdout["schema"]
        config_set = parsed_stdout["config"]

        for i in config_set:
            config_schema["properties"][i]["configured"] = config_set[i]
            config_schema["properties"][i]["latest_change"] = ".env"

    return config_schema
