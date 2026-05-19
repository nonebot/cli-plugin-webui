import json
import asyncio
from pathlib import Path
from typing import Dict, List

from nb_cli.config import ConfigManager
from packaging.requirements import Requirement
from nb_cli.cli.commands.project import ProjectContext
from nb_cli.handlers import create_project, create_virtualenv

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.models.types import ModuleType
from nb_cli_plugin_webui.app.store.dependencies import get_store_items
from nb_cli_plugin_webui.app.models.base import ModuleInfo, NoneBotProjectMeta
from nb_cli_plugin_webui.app.utils.string_utils import generate_complexity_string
from nb_cli_plugin_webui.app.handlers import NoneBotProjectManager, call_pip_install
from nb_cli_plugin_webui.app.handlers.process import (
    CustomLog,
    LogStorage,
    ProcessManager,
    LogStorageFather,
    ProcessFuncWithLog,
)

from .schemas import AddProjectData, CreateProjectData
from .exceptions import ProjectDirIsNotDir, ProjectDirAlreadyExists


def create_nonebot_project(data: CreateProjectData) -> str:
    project_name = data.project_name.replace(" ", "-")
    base_project_dir = Config.base_dir / Path(data.project_dir)
    project_dir = base_project_dir / project_name

    if NoneBotProjectManager.get_project_by_dir(str(project_dir)):
        raise ProjectDirAlreadyExists()

    drivers = [driver.project_link for driver in data.drivers]
    adapters = [adapter.project_link for adapter in data.adapters]

    # Build driver_package like "nonebot2[fastapi]>=2.5.0"
    if data.drivers:
        extras = ",".join(
            x
            for d in data.drivers
            for x in (
                d.project_link.split("[")[1].rstrip("]").split(",")
                if "[" in d.project_link
                else []
            )
        )
        driver_package = (
            f"nonebot2[{extras}]>={data.drivers[0].version}"
            if extras
            else f"nonebot2>={data.drivers[0].version}"
        )
    else:
        driver_package = "nonebot2"

    context = ProjectContext()
    context.variables["project_name"] = project_name
    context.variables["inplace"] = False
    context.variables["environment"] = {}
    context.variables["driver_package"] = f'"{driver_package}"'
    context.variables["devtools"] = ["pyright", "ruff"]
    # drivers: {project_link: driver_dict} - 单个对象
    context.variables["drivers"] = json.dumps(
        {driver.project_link: driver.model_dump() for driver in data.drivers}
    )
    context.packages.extend(
        [
            Requirement(f"{driver.project_link}>={driver.version}")
            for driver in data.drivers
        ]
    )
    # adapters: {project_link: [adapter_dict, ...]} - 列表
    _adapters: dict[str, list] = {}
    for adapter in data.adapters:
        _adapters.setdefault(adapter.project_link, []).append(adapter.model_dump())
    context.variables["adapters"] = json.dumps(_adapters)
    context.packages.extend(
        [
            Requirement(f"{adapter.project_link}>={adapter.version}")
            for adapter in data.adapters
        ]
    )

    plugin_dirs = list()
    if not data.is_bootstrap:
        context.variables["use_src"] = data.use_src
        if data.use_src:
            plugin_dirs.append("src/plugins")
        else:
            plugin_dirs.append(f"{project_name}/plugins")

    config_manager = ConfigManager(working_dir=project_dir, use_venv=True)

    log = LogStorage(Config.process_log_destroy_seconds)
    log_key = generate_complexity_string(10)
    LogStorageFather.add_storage(log, log_key)

    process = ProcessFuncWithLog(log)
    process.add(asyncio.sleep, 1)
    process.add(log.add_log, CustomLog(message="Processing at 3s..."))
    process.add(asyncio.sleep, 3)
    process.add(log.add_log, CustomLog(message=f"Project name: {project_name}"))
    process.add(log.add_log, CustomLog(message=f"Project dir: {project_dir}"))
    process.add(log.add_log, CustomLog(message=f"Mirror url: {data.mirror_url}"))
    process.add(
        log.add_log, CustomLog(message=f"Project drivers: {', '.join(drivers)}")
    )
    process.add(
        log.add_log, CustomLog(message=f"Project adapters: {', '.join(adapters)}")
    )

    process.add(log.add_log, CustomLog(message="Generate NoneBot project..."))
    process.add(
        create_project,
        "bootstrap" if data.is_bootstrap else "simple",
        {"nonebot": context.variables},
        str(base_project_dir.absolute()),
    )
    process.add(log.add_log, CustomLog(message="Finished generate."))

    process.add(log.add_log, CustomLog(message="Initialization dependencies..."))
    process.add(
        create_virtualenv, project_dir / ".venv", prompt=project_name, python_path=None
    )
    process.add(log.add_log, CustomLog(message="Finished initialization."))

    process.add(log.add_log, CustomLog(message="Install dependencies..."))

    async def install_dependencies():
        proc, _ = await call_pip_install(
            ["nonebot2", *[str(p) for p in context.packages]],
            ["-i", data.mirror_url],
            python_path=config_manager.python_path,
            log_storage=log,
        )
        await proc.wait()
        return True

    process.add(install_dependencies)
    process.add(log.add_log, CustomLog(message="Finished install."))

    async def add_project_info():
        _adapters: List[ModuleInfo] = [
            ModuleInfo.model_validate(adapter.model_dump()) for adapter in data.adapters
        ]
        _drivers: List[ModuleInfo] = [
            ModuleInfo.model_validate(driver.model_dump()) for driver in data.drivers
        ]

        project_id = generate_complexity_string(6)
        manager = NoneBotProjectManager(project_id=project_id)
        await manager.add_project(
            project_name=project_name,
            project_dir=project_dir,
            mirror_url=data.mirror_url,
            adapters=_adapters,
            drivers=_drivers,
            plugin_dirs=plugin_dirs,
        )

        manager.write_to_env(".env", "ENVIRONMENT", "prod")
        return True

    process.add(add_project_info)
    process.add(log.add_log, CustomLog(message="✨ Done!"))
    process.done()

    asyncio.get_event_loop().call_later(600, LogStorageFather.remove_storage, log_key)

    return log_key


async def add_nonebot_project(data: AddProjectData) -> str:
    project_name = data.project_name.replace(" ", "-")
    project_dir = Path(data.project_dir)
    if not project_dir.is_dir():
        raise ProjectDirIsNotDir()

    if NoneBotProjectManager.get_project_by_dir(str(project_dir)):
        raise ProjectDirAlreadyExists()

    store_plugin_data = get_store_items(ModuleType.PLUGIN, is_search=False)
    store_adapter_data = get_store_items(ModuleType.ADAPTER, is_search=False)
    store_driver_data = get_store_items(ModuleType.DRIVER, is_search=False)

    installed_plugins = list()
    for plugin in store_plugin_data:
        if plugin.module_name in data.plugins:
            installed_plugins.append(plugin)

    installed_adapters = list()
    for adapter in store_adapter_data:
        if adapter.module_name in data.adapters:
            installed_adapters.append(adapter)

    installed_drivers = list()
    for driver in store_driver_data:
        if driver.module_name in data.drivers:
            installed_drivers.append(driver)

    # Build driver_package like "nonebot2[fastapi]>=2.5.0"
    if installed_drivers:
        extras = ",".join(
            x
            for d in installed_drivers
            for x in (
                d.project_link.split("[")[1].rstrip("]").split(",")
                if "[" in d.project_link
                else []
            )
        )
        driver_package = (
            f"nonebot2[{extras}]>={installed_drivers[0].version}"
            if extras
            else f"nonebot2>={installed_drivers[0].version}"
        )
    else:
        driver_package = "nonebot2"

    context = ProjectContext()
    context.variables["project_name"] = project_name
    context.variables["inplace"] = False
    context.variables["environment"] = {}
    context.variables["driver_package"] = f'"{driver_package}"'
    context.variables["devtools"] = ["pyright", "ruff"]
    # drivers: {project_link: driver_dict} - 单个对象
    context.variables["drivers"] = json.dumps(
        {driver.project_link: driver.model_dump() for driver in installed_drivers}
    )
    context.packages.extend(
        [
            Requirement(f"{driver.project_link}>={driver.version}")
            for driver in installed_drivers
        ]
    )
    # adapters: {project_link: [adapter_dict, ...]} - 列表
    _adapters: dict[str, list] = {}
    for adapter in installed_adapters:
        _adapters.setdefault(adapter.project_link, []).append(adapter.model_dump())
    context.variables["adapters"] = json.dumps(_adapters)
    context.packages.extend(
        [
            Requirement(f"{adapter.project_link}>={adapter.version}")
            for adapter in installed_adapters
        ]
    )

    config_manager = ConfigManager(working_dir=project_dir, use_venv=True)

    log = LogStorage(Config.process_log_destroy_seconds)
    log_key = generate_complexity_string(10)
    LogStorageFather.add_storage(log, log_key)

    process = ProcessFuncWithLog(log)
    process.add(asyncio.sleep, 1)
    process.add(log.add_log, CustomLog(message="Processing at 3s..."))
    process.add(asyncio.sleep, 3)
    process.add(log.add_log, CustomLog(message=f"Project name: {project_name}"))
    process.add(log.add_log, CustomLog(message=f"Project dir: {project_dir}"))
    process.add(log.add_log, CustomLog(message=f"Mirror url: {data.mirror_url}"))
    process.add(
        log.add_log,
        CustomLog(
            message=f"Project drivers: {', '.join(d.module_name for d in installed_drivers)}"
        ),
    )
    process.add(
        log.add_log,
        CustomLog(
            message=f"Project adapters: {', '.join(a.module_name for a in installed_adapters)}"
        ),
    )
    process.add(
        log.add_log, CustomLog(message=f"Project plugins: {', '.join(data.plugins)}")
    )

    venv_path = project_dir / ".venv"
    if not venv_path.is_dir():
        process.add(
            log.add_log,
            CustomLog(message=f"Not found virtualenv in {venv_path.absolute()}"),
        )
        process.add(log.add_log, CustomLog(message="Initialization dependencies..."))
        process.add(
            create_virtualenv,
            project_dir / ".venv",
            prompt=project_name,
            python_path=None,
        )
    process.add(log.add_log, CustomLog(message="Finished initialization."))

    process.add(log.add_log, CustomLog(message="Install dependencies..."))

    async def install_dependencies():
        proc, _ = await call_pip_install(
            ["nonebot2", *[str(p) for p in context.packages]],
            ["-i", data.mirror_url],
            python_path=config_manager.python_path,
            log_storage=log,
        )
        await proc.wait()
        return True

    process.add(install_dependencies)
    process.add(log.add_log, CustomLog(message="Finished install."))

    async def add_project_info():
        _adapters: List[ModuleInfo] = [
            ModuleInfo.model_validate(adapter.model_dump())
            for adapter in installed_adapters
        ]
        _drivers: List[ModuleInfo] = [
            ModuleInfo.model_validate(driver.model_dump())
            for driver in installed_drivers
        ]

        project_id = generate_complexity_string(6)
        manager = NoneBotProjectManager(project_id=project_id)
        await manager.add_project(
            project_name=project_name,
            project_dir=project_dir,
            mirror_url=data.mirror_url,
            adapters=_adapters,
            drivers=_drivers,
            plugins=installed_plugins,
            plugin_dirs=data.plugin_dirs,
            builtin_plugins=data.builtin_plugins,
        )

        env_path = project_dir / ".env"
        if not env_path.exists() or not env_path.is_file():
            manager.write_to_env(".env", "ENVIRONMENT", "prod")

        return True

    process.add(add_project_info)
    process.add(log.add_log, CustomLog(message="✨ Done!"))
    process.done()

    asyncio.get_event_loop().call_later(600, LogStorageFather.remove_storage, log_key)

    return log_key


def list_nonebot_project() -> Dict[str, NoneBotProjectMeta]:
    try:
        project = NoneBotProjectManager.get_project()
    except Exception:
        project = dict()

    if not project:
        return project

    processes = ProcessManager.processes
    result: Dict[str, NoneBotProjectMeta] = dict()
    for project_id in project:
        _project = project.get(project_id)
        if _project is None:
            continue

        if not Path(_project.project_dir).exists():
            npm = NoneBotProjectManager(project_id=project_id)
            npm.remove_project()
            continue

        is_running = False
        for process_id in processes:
            process = processes.get(process_id)
            if process is None:
                continue

            if _project.project_id == process_id and process.process_is_running:
                is_running = True
                break

        _project.is_running = is_running
        result[project_id] = _project

    return result
