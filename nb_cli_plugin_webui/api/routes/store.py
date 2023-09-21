# flake8:noqa: F401
from nb_cli.handlers import list_builtin_plugins
from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.exceptions import NonebotProjectIsNotExist
from nb_cli_plugin_webui.api.dependencies.project import NonebotProjectManager
from nb_cli_plugin_webui.models.schemas.store import (
    StoreListResponse,
    StoreSearchRequest,
)
from nb_cli_plugin_webui.api.dependencies.store.manage import (
    DRIVER_MANAGER,
    PLUGIN_MANAGER,
    ADAPTER_MANAGER,
)

router = APIRouter()


@router.get("/list/plugin", response_model=StoreListResponse)
async def get_nonebot_store_plugins(
    project_id: str, page: int, is_search: int, show_all: int = 0
) -> StoreListResponse:
    project = NonebotProjectManager(project_id)
    try:
        project_info = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="实例不存在")

    if show_all:
        data = PLUGIN_MANAGER.get_item(is_search=bool(is_search))
    else:
        data = PLUGIN_MANAGER.generate_page(
            project_info, page=page, is_search=bool(is_search)
        )

    return StoreListResponse(
        now_page=int(page),
        total_page=PLUGIN_MANAGER.get_max_page(is_search=bool(is_search)),
        total_item=len(PLUGIN_MANAGER.get_item(is_search=bool(is_search))),
        data=data,
    )


@router.get("/list/builtin_plugin", response_model=StoreListResponse)
async def get_nonebot_builtin_plugins(project_id: str) -> StoreListResponse:
    project = NonebotProjectManager(project_id)
    try:
        project.read()
    except NonebotProjectIsNotExist:
        raise NonebotProjectIsNotExist

    data = await list_builtin_plugins(python_path=project.config_manager.python_path)

    return StoreListResponse(
        now_page=0,
        total_page=0,
        total_item=0,
        data=data,
    )


@router.get("/list/adapter", response_model=StoreListResponse)
async def get_nonebot_store_adapters(
    project_id: str, page: int, is_search: int, show_all: int = 0
) -> StoreListResponse:
    project = NonebotProjectManager(project_id)
    try:
        project_info = project.read()
    except NonebotProjectIsNotExist:
        project_info = None

    if show_all:
        data = ADAPTER_MANAGER.get_item(is_search=bool(is_search))
    else:
        data = ADAPTER_MANAGER.generate_page(
            project_info, page=page, is_search=bool(is_search)
        )

    return StoreListResponse(
        now_page=int(page),
        total_page=ADAPTER_MANAGER.get_max_page(is_search=bool(is_search)),
        total_item=len(ADAPTER_MANAGER.get_item(is_search=bool(is_search))),
        data=data,
    )


@router.get("/list/driver", response_model=StoreListResponse)
async def get_nonebot_store_drivers(
    project_id: str, page: int, is_search: int, show_all: int = 0
) -> StoreListResponse:
    project = NonebotProjectManager(project_id)
    try:
        project_info = project.read()
    except NonebotProjectIsNotExist:
        project_info = None

    if show_all:
        data = DRIVER_MANAGER.get_item(is_search=bool(is_search))
    else:
        data = DRIVER_MANAGER.generate_page(
            project_info, page=page, is_search=bool(is_search)
        )

    return StoreListResponse(
        now_page=int(page),
        total_page=DRIVER_MANAGER.get_max_page(is_search=bool(is_search)),
        total_item=len(DRIVER_MANAGER.get_item(is_search=bool(is_search))),
        data=data,
    )


@router.get("/list/refresh")
async def refresh_nonebot_store_module():
    await PLUGIN_MANAGER.load_item()
    await ADAPTER_MANAGER.load_item()
    await DRIVER_MANAGER.load_item()


@router.post("/search", response_model=StoreListResponse)
async def search_nonebot_store(
    data: StoreSearchRequest = Body(embed=True),
) -> StoreListResponse:
    project = NonebotProjectManager(data.project_id)
    try:
        project_info = project.read()
    except NonebotProjectIsNotExist:
        raise NonebotProjectIsNotExist

    if data.module_type == "plugin":
        PLUGIN_MANAGER.search_item(project_info, data.content)
        result = PLUGIN_MANAGER.generate_page(project_info, page=0, is_search=True)
        total_item = len(PLUGIN_MANAGER.search_result)
        total_page = PLUGIN_MANAGER.get_max_page(is_search=True)
    elif data.module_type == "adapter":
        ADAPTER_MANAGER.search_item(project_info, data.content)
        result = ADAPTER_MANAGER.generate_page(project_info, page=0, is_search=True)
        total_item = len(ADAPTER_MANAGER.search_result)
        total_page = ADAPTER_MANAGER.get_max_page(is_search=True)
    else:
        DRIVER_MANAGER.search_item(project_info, data.content)
        result = DRIVER_MANAGER.generate_page(project_info, page=0, is_search=True)
        total_item = len(DRIVER_MANAGER.search_result)
        total_page = DRIVER_MANAGER.get_max_page(is_search=True)

    return StoreListResponse(
        now_page=int(), total_page=total_page, total_item=total_item, data=result
    )
