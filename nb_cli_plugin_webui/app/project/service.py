import json
import asyncio
from pathlib import Path
from typing import Dict, List

from nb_cli.config import ConfigManager
from nb_cli.cli.commands.project import ProjectContext
from nb_cli.handlers import create_project, create_virtualenv

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.store.dependencies import get_store_items
from nb_cli_plugin_webui.app.schemas import ModuleInfo, NoneBotProjectMeta
from nb_cli_plugin_webui.app.utils.string_utils import generate_complexity_string
from nb_cli_plugin_webui.app.handlers import NoneBotProjectManager, call_pip_install
from nb_cli_plugin_webui.app.handlers.process import (
    CustomLog,
    LogStorage,
    ProcessManager,
    LogStorageFather,
    ProcessFuncWithLog,
)

from .exceptions import ProjectDirIsNotDir
from .schemas import AddProjectData, CreateProjectData


def create_nonebot_project(data: CreateProjectData) -> str:
    project_name = data.project_name.replace(" ", "-")
    base_project_dir = Config.base_dir / Path(data.project_dir)
    project_dir = base_project_dir / project_name
    drivers = [driver.project_link for driver in data.drivers]
    adapters = [adapter.project_link for adapter in data.adapters]

    context = ProjectContext()
    context.variables["project_name"] = project_name
    context.variables["drivers"] = json.dumps(
        {driver.project_link: driver.dict() for driver in data.drivers}
    )
    context.packages.extend(drivers)
    context.variables["adapters"] = json.dumps(
        {adapter.project_link: adapter.dict() for adapter in data.adapters}
    )
    context.packages.extend(adapters)

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
            ["nonebot2", *context.packages],
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
            ModuleInfo.parse_obj(adapter.dict()) for adapter in data.adapters
        ]
        _drivers: List[ModuleInfo] = [
            ModuleInfo.parse_obj(driver.dict()) for driver in data.drivers
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

    store_plugin_data = get_store_items("plugin", is_search=False)
    store_adapter_data = get_store_items("adapter", is_search=False)

    installed_plugins = list()
    for plugin in store_plugin_data:
        if plugin.module_name in data.plugins:
            installed_plugins.append(plugin)

    installed_adapters = list()
    for adapter in store_adapter_data:
        if adapter.module_name in data.adapters:
            installed_adapters.append(adapter)

    context = ProjectContext()
    context.variables["project_name"] = project_name
    context.variables["adapters"] = json.dumps(
        {adapter.project_link: adapter.dict() for adapter in installed_adapters}
    )
    context.packages.extend([adapter.project_link for adapter in installed_adapters])

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
        log.add_log, CustomLog(message=f"Project plugins: {', '.join(data.plugins)}")
    )
    process.add(
        log.add_log, CustomLog(message=f"Project adapters: {', '.join(data.adapters)}")
    )
    process.add(log.add_log, CustomLog(message=str()))

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
            ["nonebot2", *context.packages],
            ["-i", data.mirror_url],
            python_path=config_manager.python_path,
            log_storage=log,
        )
        await proc.wait()
        return True

    process.add(install_dependencies)
    process.add(log.add_log, CustomLog(message="Finished install."))

    project_id = generate_complexity_string(6)
    manager = NoneBotProjectManager(project_id=project_id)
    await manager.add_project(
        project_name=project_name,
        project_dir=project_dir,
        mirror_url=data.mirror_url,
        adapters=installed_adapters,
        plugins=installed_plugins,
    )
    manager.read()
    for plugin in installed_plugins:
        await manager.add_plugin(plugin)

    env_path = project_dir / ".env"
    if not env_path.exists() or not env_path.is_file():
        manager.write_to_env(".env", "ENVIRONMENT", "prod")

    process.add(log.add_log, CustomLog(message="✨ Done!"))
    process.done()

    asyncio.get_event_loop().call_later(600, LogStorageFather.remove_storage, log_key)

    return log_key


def list_nonebot_project() -> Dict[str, NoneBotProjectMeta]:
    try:
        projects = NoneBotProjectManager.get_projects()
    except Exception:
        projects = dict()

    if not projects:
        return projects

    processes = ProcessManager.processes
    result: Dict[str, NoneBotProjectMeta] = dict()
    for project_id in projects:
        project = projects.get(project_id)
        if project is None:
            continue

        if not Path(project.project_dir).exists():
            npm = NoneBotProjectManager(project_id=project_id)
            npm.remove_project()
            continue

        is_running = False
        for process_id in processes:
            process = processes.get(process_id)
            if process is None:
                continue

            if project.project_id == process_id and process.process_is_running:
                is_running = True
                break

        project.is_running = is_running
        result[project_id] = project

    return result
