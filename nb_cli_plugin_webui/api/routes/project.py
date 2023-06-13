import shutil
import asyncio
from pathlib import Path

from nb_cli.config import ConfigManager
from nb_cli.handlers.project import create_project
from nb_cli.handlers.venv import create_virtualenv
from nb_cli.cli.commands.project import ProjectContext
from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.api.dependencies.files import BASE_DIR
from nb_cli_plugin_webui.utils import generate_complexity_string
from nb_cli_plugin_webui.api.dependencies.pip import call_pip_install
from nb_cli_plugin_webui.models.domain.process import LogLevel, CustomLog
from nb_cli_plugin_webui.api.dependencies.project import NonebotProjectManager
from nb_cli_plugin_webui.api.dependencies.process.log import (
    LoggerStorage,
    LoggerStorageFather,
)
from nb_cli_plugin_webui.models.schemas.project import (
    CreateProjectData,
    ProjectListResponse,
    CreateProjectResponse,
    DeleteProjectResponse,
)

router = APIRouter()


@router.post("/create", response_model=CreateProjectResponse)
async def create_nonebot_project(
    project_data: CreateProjectData = Body(embed=True),
) -> CreateProjectResponse:
    project_name = project_data.project_name.replace(" ", "-")

    context = ProjectContext()
    context.variables["project_name"] = project_name
    context.variables["drivers"] = [project_data.driver.dict()]
    context.variables["adapters"] = [project_data.adapter.dict()]
    context.packages.extend([project_data.adapter.project_link])

    base_project_dir = BASE_DIR / Path(project_data.project_dir)
    project_dir = base_project_dir / project_name

    # TODO: simple context

    log = LoggerStorage()
    log_key = generate_complexity_string(6)
    LoggerStorageFather.add_storage(log, log_key)

    async def notice(log: LoggerStorage):
        async def _err_parse(err: Exception):
            log_model = CustomLog(level=LogLevel.ERROR, message=str(err))
            await log.add_log(log_model)

            shutil.rmtree(project_dir)

            log_model = CustomLog(message="All files about project have been cleared.")
            await log.add_log(log_model)

            log_model = CustomLog(message="❗ Failed...")
            await log.add_log(log_model)

        # Time for frontend ready
        await asyncio.sleep(1)

        log_model = CustomLog(message="Processing at 3s...")
        await log.add_log(log_model)

        await asyncio.sleep(3)

        log_model = CustomLog(message=f"Project name: {project_data.project_name}")
        await log.add_log(log_model)

        log_model = CustomLog(message=f"Project Dir: {project_dir.absolute()}")
        await log.add_log(log_model)

        log_model = CustomLog(message=f"Project Driver: {project_data.driver.name}")
        await log.add_log(log_model)

        log_model = CustomLog(message=f"Project Adapter: {project_data.adapter.name}")
        await log.add_log(log_model)

        log_model = CustomLog(message=str())
        await log.add_log(log_model)

        try:
            log_model = CustomLog(message="Generate NoneBot project files...")
            await log.add_log(log_model)

            create_project(
                "bootstrap",
                {"nonebot": context.variables},
                str(base_project_dir.absolute()),
            )

            log_model = CustomLog(message="Finished generate NoneBot project files")
            await log.add_log(log_model)
        except Exception as err:
            await _err_parse(err)
            return

        try:
            log_model = CustomLog(message="Initialization dependencies...")
            await log.add_log(log_model)

            venv_dir = project_dir / ".venv"
            await create_virtualenv(venv_dir, prompt=project_name, python_path=None)
        except Exception as err:
            await _err_parse(err)
            return

        config_manager = ConfigManager(working_dir=project_dir, use_venv=True)

        try:
            log_model = CustomLog(message="Installing dependencies...")
            await log.add_log(log_model)

            proc, log = await call_pip_install(
                ["nonebot2", *context.packages],
                ["-i", project_data.mirror_url],
                log_storage=log,
                python_path=config_manager.python_path,
            )
            await proc.wait()
        except Exception as err:
            await _err_parse(err)
            return

        project_id = generate_complexity_string(6)
        manager = NonebotProjectManager(project_id=project_id)
        manager.add(
            project_name=project_name,
            project_dir=project_dir,
            mirror_url=project_data.mirror_url,
            adapters=[project_data.adapter],
            drivers=[project_data.driver],
        )

        log_model = CustomLog(message="✨ Done!")
        await log.add_log(log_model)

    asyncio.create_task(notice(log))

    return CreateProjectResponse(log_key=log_key)


@router.post("/delete", response_model=DeleteProjectResponse)
async def delete_nonebot_project(project_id: str) -> DeleteProjectResponse:
    manager = NonebotProjectManager(project_id=project_id)
    data = manager.read()

    try:
        shutil.rmtree(data.project_dir)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    manager.remove()

    return DeleteProjectResponse(project_id=project_id)


@router.get("/list", response_model=ProjectListResponse)
async def get_nonebot_projects() -> ProjectListResponse:
    try:
        return ProjectListResponse(projects=NonebotProjectManager.get_projects())
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
