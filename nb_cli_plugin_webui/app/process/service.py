import os
import sys
from typing import List
from pathlib import Path

from nb_cli.config import SimpleInfo as CliSimpleInfo
from nb_cli.handlers import get_default_python, generate_run_script

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.project import service as project_service
from nb_cli_plugin_webui.app.handlers.process import (
    Processor,
    ProcessManager,
    LogStorageFather,
    ProcessAlreadyRunning,
)

from .exceptions import DriverNotFound, AdapterNotFound


async def run_nonebot_project(project: project_service.NoneBotProjectManager):
    project_meta = project.read()
    if not project_meta.adapters:
        raise AdapterNotFound()
    if not project_meta.drivers:
        raise DriverNotFound()

    project_dir = Path(project_meta.project_dir)
    env = os.environ.copy()
    env["TERM"] = "xterm-color"
    if sys.platform == "win32":
        venv_path = project_dir / Path(".venv/Scripts")
        env["PATH"] = f"{venv_path.absolute()};{env['PATH']}"
    else:
        venv_path = project_dir / Path(".venv/bin")
        env["PATH"] = f"{venv_path.absolute()}:{env['PATH']}"

    process = ProcessManager.get_process(project_meta.project_id)
    if process:
        if process.process_is_running:
            raise ProcessAlreadyRunning()
        else:
            await process.start()
    else:
        python_path = project.config_manager.python_path
        if python_path is None:
            python_path = await get_default_python()

        raw_adapters = project_meta.adapters
        adapters: List[CliSimpleInfo] = list()
        for adapter in raw_adapters:
            adapters.append(
                CliSimpleInfo(name=adapter.name, module_name=adapter.module_name)
            )
        run_script = await generate_run_script(
            adapters=adapters,
            builtin_plugins=project_meta.builtin_plugins,
        )

        log_destroy_time = Config.process_log_destroy_seconds
        if project_meta.use_run_script:
            run_script_file = project_dir / project_meta.run_script_name
            if not run_script_file.exists():
                run_script_file.write_text(run_script, encoding="utf-8")

            process = Processor(
                python_path,
                run_script_file,
                cwd=project_dir,
                env=env,
                log_destroy_seconds=log_destroy_time,
            )
        else:
            process = Processor(
                python_path,
                "-c",
                run_script,
                cwd=project_dir,
                env=env,
                log_destroy_seconds=log_destroy_time,
            )

        LogStorageFather.add_storage(process.log_storage, project_meta.project_id)
        ProcessManager.add_process(process, project_meta.project_id)
        await process.start()
