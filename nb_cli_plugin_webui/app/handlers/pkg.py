from typing import Optional

from nb_cli.handlers import get_default_python

from nb_cli_plugin_webui.app.utils.process import run_python_script

from . import templates


async def get_pkg_version(package: str, python_path: Optional[str] = None) -> str:
    """获取实例环境中所安装的包的版本

    Returns:
        str: 包的版本
    """
    if python_path is None:
        python_path = await get_default_python()

    t = templates.get_template("scripts/script/get_pkg_version.py.jinja")
    raw_content = await run_python_script(
        python_path, await t.render_async(package=package)
    )

    return raw_content.strip()
