import shutil
from typing import List

from fastapi import Depends, APIRouter

from nb_cli_plugin_webui.app.logging import logger as log
from nb_cli_plugin_webui.app.handlers import NoneBotProjectManager
from nb_cli_plugin_webui.app.models.base import Plugin, ModuleInfo, NoneBotProjectMeta

from .exceptions import ProjectDeleteFailed
from .config.router import router as config_router
from .dependencies import get_nonebot_project_toml, get_nonebot_project_manager
from .service import add_nonebot_project, list_nonebot_project, create_nonebot_project
from .schemas import (
    AddProjectData,
    GenericResponse,
    CreateProjectData,
    ProjectTomlDetail,
    ListProjectResponse,
)

router = APIRouter(tags=["project"])
router.include_router(config_router, prefix="/config")


@router.post("/create", response_model=GenericResponse[str])
async def create_project(data: CreateProjectData) -> GenericResponse[str]:
    """
    - 创建 NoneBot 实例
    - 返回对应的日志密钥, 用于日志展现
    """
    result = create_nonebot_project(data)
    return GenericResponse(detail=result)


@router.post("/add", response_model=GenericResponse[str])
async def add_project(data: AddProjectData) -> GenericResponse[str]:
    """
    - 添加 NoneBot 实例
    - 返回对应的日志密钥, 用于日志展现
    """
    result = await add_nonebot_project(data)
    return GenericResponse(detail=result)


@router.get("/profile", response_model=GenericResponse[NoneBotProjectMeta])
async def get_project_profile(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[NoneBotProjectMeta]:
    """
    - 获取 NoneBot 实例的配置信息
    """
    result = project.read()
    return GenericResponse(detail=result)


@router.delete("/delete", response_model=GenericResponse[str])
async def delete_project(
    delete_fully: bool = False,
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[str]:
    """
    - 删除 NoneBot 实例
    """
    data = project.read()
    if delete_fully:
        try:
            shutil.rmtree(data.project_dir)
        except OSError as err:
            log.error(f"Delete nonebot project failed: {err}")
            log.exception(err)
            raise ProjectDeleteFailed()
    project.remove_project()
    return GenericResponse(detail="success")


@router.get("/list", response_model=ListProjectResponse)
async def list_project() -> ListProjectResponse:
    """
    - 获取所有 NoneBot 实例基本信息
    """
    result = list_nonebot_project()
    return ListProjectResponse(detail=result)


@router.post("/check_toml", response_model=GenericResponse[ProjectTomlDetail])
async def check_project_toml(
    toml_data: ProjectTomlDetail = Depends(get_nonebot_project_toml),
) -> GenericResponse[ProjectTomlDetail]:
    """
    - 检查 NoneBot 实例的 toml 文件并从中获取所需信息
    """

    return GenericResponse(detail=toml_data)


@router.get("/plugins", response_model=GenericResponse[List[Plugin]])
async def get_plugins(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[List[Plugin]]:
    """
    - 获取实例的插件列表
    """
    project_metadata = project.read()
    return GenericResponse(detail=project_metadata.plugins)


@router.get("/adapters", response_model=GenericResponse[List[ModuleInfo]])
async def get_adapters(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[List[ModuleInfo]]:
    """
    - 获取实例的适配器列表
    """
    project_metadata = project.read()
    return GenericResponse(detail=project_metadata.adapters)


@router.get("/drivers", response_model=GenericResponse[List[ModuleInfo]])
async def get_drivers(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[List[ModuleInfo]]:
    """
    - 获取实例的驱动器列表
    """
    project_metadata = project.read()
    return GenericResponse(detail=project_metadata.drivers)
