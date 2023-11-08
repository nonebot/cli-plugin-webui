import json
import asyncio
from pathlib import Path
from typing import Optional

from nb_cli.handlers import create_process, get_default_python

from . import templates


async def get_nonebot_config_detail(
    cwd: Optional[Path] = None, python_path: Optional[str] = None
):
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/nonebot/get_nonebot_config_detail.py.jinja")

    proc = await create_process(
        python_path,
        "-c",
        await t.render_async(),
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    parsed_stdout = json.loads(stdout.strip())

    config_schema = parsed_stdout["schema"]
    config_set = parsed_stdout["config"]

    for i in config_set:
        if config_schema["properties"].get(i) is None:
            continue

        config_schema["properties"][i]["configured"] = config_set[i]
        config_schema["properties"][i]["latest_change"] = ".env"

    return config_schema
