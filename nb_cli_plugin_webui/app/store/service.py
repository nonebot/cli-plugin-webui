import re
import asyncio
from typing import Union, Annotated

from pydantic import Field
from nb_cli.handlers import call_pip_uninstall

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.handlers import call_pip_install
from nb_cli_plugin_webui.app.project import service as project_service
from nb_cli_plugin_webui.app.utils.string_utils import generate_complexity_string
from nb_cli_plugin_webui.app.project.exceptions import WriteNoneBotProjectProfileFailed
from nb_cli_plugin_webui.app.handlers.process import (
    CustomLog,
    LogStorage,
    LogStorageFather,
    ProcessFuncWithLog,
)

from .schemas import Plugin, ModuleInfo
from .exception import ModuleNotFound, ModuleIsExisted, ModuleTypeNotFound


def install_nonebot_module(
    project: project_service.NoneBotProjectManager,
    env: str,
    module: Annotated[Union[ModuleInfo, Plugin], Field(discriminator="module_type")],
) -> str:
    project_meta = project.read()
    if isinstance(module, Plugin):
        for plugin in project_meta.plugins:
            if module.module_name == plugin.module_name:
                raise ModuleIsExisted()
    elif isinstance(module, ModuleInfo):
        for adapter in project_meta.adapters:
            if module.module_name == adapter.module_name:
                raise ModuleIsExisted()
        for driver in project_meta.drivers:
            if module.module_name == driver.module_name:
                raise ModuleIsExisted()

    module_type = "driver"
    if "~" not in module.module_name:
        pattern = r"nonebot-(.*?)-"
        _match = re.search(pattern, module.project_link)
        if _match is None:
            raise ModuleTypeNotFound()
        module_type = _match.group(1)

    log = LogStorage(Config.process_log_destroy_seconds)
    log_key = generate_complexity_string(8)
    LogStorageFather.add_storage(log, log_key)

    process = ProcessFuncWithLog(log)
    process.add(asyncio.sleep, 1)
    process.add(log.add_log, CustomLog(message="Processing at 3s..."))
    process.add(asyncio.sleep, 3)
    process.add(
        log.add_log, CustomLog(message=f"Install module name: {module.module_name}")
    )

    async def install_module():
        proc, _ = await call_pip_install(
            module.project_link,
            ["-i", project_meta.mirror_url],
            log_storage=log,
            python_path=project.config_manager.python_path,
        )
        await proc.wait()
        return True

    process.add(install_module)

    async def write_to_project_profile():
        if module_type == "plugin" and isinstance(module, Plugin):
            await project.add_plugin(module)
        elif module_type == "adapter":
            project.add_adapter(module)
        elif module_type == "driver":
            project.add_driver(env, module)
        return True

    process.add(write_to_project_profile)
    process.add(log.add_log, CustomLog(message="✨ Done!"))
    process.done()

    return log_key


async def uninstall_nonebot_module(
    project: project_service.NoneBotProjectManager,
    env: str,
    module: Annotated[Union[ModuleInfo, Plugin], Field(discriminator="module_type")],
) -> None:
    if isinstance(module, Plugin):
        for plugin in project.read().plugins:
            if module.module_name == plugin.module_name:
                break
        else:
            raise ModuleNotFound()
    elif isinstance(module, ModuleInfo):
        for adapter in project.read().adapters:
            if module.module_name == adapter.module_name:
                break
        else:
            for driver in project.read().drivers:
                if module.module_name == driver.module_name:
                    break
            else:
                raise ModuleNotFound()

    async def _call_pip_uninstall(package) -> None:
        proc = await call_pip_uninstall(
            package,
            ["-y"],
            python_path=project.config_manager.python_path,
            stdout=asyncio.subprocess.PIPE,
        )
        await proc.wait()

    project_meta = project.read()
    package: str = module.project_link
    if package.startswith("nonebot2[") and package.endswith("]"):
        package = package[9:-1]

    onebot_adapter_prefix = "nonebot.adapters.onebot"
    if module.module_name.startswith(onebot_adapter_prefix):
        onebot_adapter_count = int()
        for adapter in project_meta.adapters:
            if adapter.module_name.startswith(onebot_adapter_prefix):
                onebot_adapter_count += 1

        if onebot_adapter_count == 1:
            await _call_pip_uninstall(package)
    else:
        await _call_pip_uninstall(package)

    module_type = None
    pattern = r"nonebot-(.*?)-"
    _match = re.search(pattern, package)
    if _match:
        module_type = _match.group(1)

    pattern = r"~(.*?)"
    _match = re.search(pattern, module.module_name)
    if _match:
        module_type = "driver"

    if module_type is None:
        raise ModuleTypeNotFound()

    try:
        if module_type == "plugin" and isinstance(module, Plugin):
            project.remove_plugin(module)
        elif module_type == "adapter":
            project.remove_adapter(module)
        elif module_type == "driver":
            project.remove_driver(env, module)
    except Exception:
        raise WriteNoneBotProjectProfileFailed()
