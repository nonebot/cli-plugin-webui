from typing import Union, Optional

from fastapi import Body, Depends, APIRouter

from nb_cli_plugin_webui.app.schemas import GenericResponse
from nb_cli_plugin_webui.app.handlers import NoneBotProjectManager
from nb_cli_plugin_webui.app.project import get_nonebot_project_manager

from .utils import get_store_manager
from .schemas import Plugin, ModuleInfo, StoreListResponse
from .service import install_nonebot_module, uninstall_nonebot_module

router = APIRouter()


@router.post("/nonebot/install", response_model=GenericResponse[str])
async def _install_nonebot_module(
    env: str,
    module: Union[ModuleInfo, Plugin] = Body(..., discriminator="module_type"),
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[str]:
    """
    - 安装模块至 NoneBot 实例
    """
    log_key = install_nonebot_module(project, env, module)
    return GenericResponse(detail=log_key)


@router.post("/nonebot/uninstall", response_model=GenericResponse[str])
async def _uninstall_nonebot_module(
    env: str,
    module: Union[ModuleInfo, Plugin] = Body(..., discriminator="module_type"),
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[str]:
    """
    - 卸载 NoneBot 实例中的模块
    """
    await uninstall_nonebot_module(project, env, module)
    return GenericResponse(detail="success")


@router.get("/nonebot/list", response_model=StoreListResponse)
async def _get_nonebot_store_items(
    module_type: str,
    page: int,
    is_search: bool = False,
    show_all: bool = False,
    project_id: Optional[str] = None,
) -> StoreListResponse:
    """
    - 获取 NoneBot Store 中的模块列表
    """
    project = None
    project_meta = None
    try:
        if project_id:
            project = get_nonebot_project_manager(project_id)
            project_meta = project.read()
    except Exception:
        pass

    store_manager = get_store_manager(module_type)
    if not show_all:
        data = store_manager.generate_page(project_meta, page=page, is_search=is_search)
    else:
        data = store_manager.get_item(is_search=is_search)

    return StoreListResponse(
        now_page=int(page),
        total_page=store_manager.get_max_page(is_search=is_search),
        total_item=len(store_manager.get_item(is_search=is_search)),
        detail=data,
    )


@router.post("/nonebot/search", response_model=StoreListResponse)
async def search_nonebot_store_item(
    module_type: str,
    content: str,
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> StoreListResponse:
    """
    - 搜索 NoneBot Store 中的模块
    """
    project_meta = project.read()
    store_manager = get_store_manager(module_type)

    store_manager.search_item(project_meta, content=content)
    result = store_manager.generate_page(project_meta, page=0, is_search=True)
    total_page = store_manager.get_max_page(is_search=True)
    total_item = len(store_manager.search_result)

    return StoreListResponse(
        now_page=int(),
        total_page=total_page,
        total_item=total_item,
        detail=result,
    )
