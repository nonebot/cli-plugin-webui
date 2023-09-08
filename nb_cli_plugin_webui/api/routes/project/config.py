import ast
import json
from typing import List
from pathlib import Path

from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.exceptions import NonebotProjectIsNotExist
from nb_cli_plugin_webui.api.dependencies.project import NonebotProjectManager
from nb_cli_plugin_webui.api.dependencies.nonebot import get_nonebot_config_detail
from nb_cli_plugin_webui.models.schemas.project import (
    ModuleConfigChild,
    DotenvListResponse,
    ModuleConfigFather,
    NonebotProjectMeta,
    ModuleConfigResponse,
    ModuleSettingRequest,
)

router = APIRouter()


@router.get("/dotenv/list", response_model=DotenvListResponse)
async def get_dotenv_file_list(project_id: str) -> DotenvListResponse:
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    project_dir = Path(project_detail.project_dir)
    cache_list = list()
    for i in project_dir.iterdir():
        if ".env" in i.name:
            cache_list.append(i.name)

    return DotenvListResponse(detail=cache_list)


@router.post("/dotenv/create")
async def create_dotenv_file(
    project_id: str = Body(embed=True), env: str = Body(embed=True)
):
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    project_dir = Path(project_detail.project_dir)
    for i in project_dir.iterdir():
        if env == i.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="已存在相同的文件"
            )

    with open(project_dir / env, "w", encoding="utf-8") as w:
        w.write(str())

    return {"detail": "OK"}


@router.post("/dotenv/delete")
async def delete_dotenv_file(
    project_id: str = Body(embed=True), env: str = Body(embed=True)
):
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    project_dir = Path(project_detail.project_dir)
    for i in project_dir.iterdir():
        if env == i.name:
            i.unlink()
            return {"detail": "OK"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件未找到")


@router.post("/dotenv/active")
async def active_dotenv_file(
    project_id: str = Body(embed=True), env: str = Body(embed=True)
):
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    project_dir = Path(project_detail.project_dir)
    for i in project_dir.iterdir():
        if env == i.name:
            project.write_to_env(".env", "ENVIRONMENT", env.replace(".env.", str()))
            return {"detail": "OK"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未找到对应的设置项")


@router.get("/meta/list", response_model=ModuleConfigResponse)
async def get_meta_config_list(project_id: str) -> ModuleConfigResponse:
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    config_props = NonebotProjectMeta.schema()["properties"]
    cache_list: List[ModuleConfigChild] = list()
    for prop in config_props:
        if prop not in project.meta_modifiable_key:
            continue

        prop_detail = config_props[prop]
        item_type = prop_detail.get("type", "string")

        detail = ModuleConfigChild(
            title=prop_detail["title"],
            description=str(),
            name=prop,
            default=str(),
            item_type=item_type,
            enum=list(),
            configured=getattr(project_detail, prop),
        )
        cache_list.append(detail)

    result = ModuleConfigFather(
        title="Project Config",
        description=str(),
        name="project-meta",
        properties=cache_list,
    )

    return ModuleConfigResponse(detail=[result])


@router.get("/nonebot/list", response_model=ModuleConfigResponse)
async def get_nonebot_config_list(project_id: str) -> ModuleConfigResponse:
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    try:
        config_detail = await get_nonebot_config_detail(
            Path(project_detail.project_dir), project.config_manager.python_path
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="获取 Nonebot 配置失败"
        )

    config_props = config_detail["properties"]
    cache_list: List[ModuleConfigChild] = list()
    for prop in config_props:
        prop_detail = config_props[prop]
        default_param = prop_detail["default"]
        item_type = prop_detail.get("type", "string")
        enum = list()

        detail = ModuleConfigChild(
            title=prop_detail["title"],
            description=prop_detail.get("description", str()),
            name=prop,
            default=[str(i) for i in default_param]
            if type(default_param) in [list, set]
            else default_param,
            item_type=item_type,
            enum=enum,
            configured=prop_detail["configured"],
        )
        cache_list.append(detail)

    result = ModuleConfigFather(
        title="Nonebot Config",
        description=config_detail.get("description", str()),
        name="nonebot-config",
        properties=cache_list,
    )

    return ModuleConfigResponse(detail=[result])


@router.get("/plugin/list", response_model=ModuleConfigResponse)
async def get_plugin_config_list(project_id: str) -> ModuleConfigResponse:
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    plugin_list = project_detail.plugins
    result: List[ModuleConfigFather] = list()
    for plugin in plugin_list:
        config_detail = plugin.config_detail

        detail_props = config_detail.get("properties")
        if detail_props is None:
            continue

        cache_list: List[ModuleConfigChild] = list()
        for prop in detail_props:
            item_type = detail_props[prop]["type"]
            if item_type == "object":
                configured = str(detail_props[prop]["configured"])
                default_param = configured
            else:
                configured = detail_props[prop]["configured"]
                default_param = detail_props[prop]["default"]

            default_value = (
                [str(i) for i in default_param]
                if type(default_param) in [list, set]
                else default_param
            )

            enum = list()
            items = detail_props[prop].get("items")
            if items and item_type == "array":
                enum = items.get("enum", list())

            config_detail = ModuleConfigChild(
                title=detail_props[prop]["title"],
                description=detail_props[prop].get("description", str()),
                name=prop,
                default=default_value,
                item_type=item_type,
                enum=enum,
                configured=configured,
                latest_change=detail_props[prop]["latest_change"],
            )
            cache_list.append(config_detail)

        plugin_detail = ModuleConfigFather(
            title=plugin.module_name,
            description=plugin.desc,
            name=plugin.module_name,
            properties=cache_list,
        )
        result.append(plugin_detail)

    return ModuleConfigResponse(detail=result)


@router.post("/set")
async def write_dotenv_file(
    project_id: str = Body(embed=True),
    module_type: str = Body(embed=True),
    data: ModuleSettingRequest = Body(embed=True),
):
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    if module_type == "project":
        if data.k_type == "boolean":
            setattr(data, "v", bool(data.v))

        target_config = data.k.split(":")[-1]
        project.modify_meta(target_config, data.v)
        return

    project_dir = Path(project_detail.project_dir)
    for i in project_dir.iterdir():
        if data.env == i.name:
            target_config = data.k.split(":")[-1]

            data.v = str(data.v)
            if data.k_type in {"object", "array", "boolean"}:
                data.v = ast.literal_eval(data.v)
                v = json.dumps(data.v)
            else:
                v = data.v
            project.write_to_env(data.env, target_config, v)

            if module_type == "nonebot_plugin":
                plugin_list = project_detail.plugins
                for plugin in plugin_list:
                    config_detail = plugin.config_detail

                    detail_props = config_detail.get("properties")
                    if detail_props is None:
                        continue

                    for prop in detail_props:
                        if target_config != prop:
                            continue

                        conf = detail_props[prop].get("configured")
                        if conf is None:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="未找到对应的设置项",
                            )
                        plugin.config_detail["properties"][prop]["configured"] = data.v
                        plugin.config_detail["properties"][prop][
                            "latest_change"
                        ] = data.env

                        project_detail.plugins = plugin_list
                        project.store(project_detail)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未找到实例位置")
