import ast
import json
from typing import List
from pathlib import Path

from fastapi import Depends, APIRouter, HTTPException, status

from nb_cli_plugin_webui.app.logging import logger as log
from nb_cli_plugin_webui.app.schemas import NoneBotProjectMeta
from nb_cli_plugin_webui.app.handlers import (
    NoneBotProjectManager,
    get_nonebot_config_detail,
)

from ..dependencies import get_nonebot_project_manager
from .exceptions import EnvExists, EnvNotFound, ConfigNotFound, BaseEnvCannotBeDeleted
from .schemas import (
    GenericResponse,
    ModuleConfigChild,
    ModuleConfigFather,
    ModuleConfigResponse,
    ModuleConfigUpdateRequest,
)

router = APIRouter()


@router.get("/env/list", response_model=GenericResponse[List[str]])
async def _get_project_env_list(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[List[str]]:
    """
    - 获取 NoneBot 实例中的环境文件列表
    """
    project_meta = project.read()
    project_dir = Path(project_meta.project_dir)
    result = list()
    for i in project_dir.iterdir():
        if i.name.startswith(".env"):
            result.append(i.name)

    return GenericResponse(detail=result)


@router.post("/env/create", response_model=GenericResponse[str])
async def _create_project_env(
    env: str,
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[str]:
    """
    - 创建 NoneBot 实例中的环境文件
    """
    project_meta = project.read()
    project_dir = Path(project_meta.project_dir)
    for i in project_dir.iterdir():
        if env == i.name:
            raise EnvExists()

    (project_dir / env).write_text(str(), encoding="utf-8")

    return GenericResponse(detail="success")


@router.delete("/env/delete", response_model=GenericResponse[str])
async def _delete_project_env(
    env: str, project: NoneBotProjectManager = Depends(get_nonebot_project_manager)
) -> GenericResponse[str]:
    """
    - 删除 NoneBot 实例中的环境文件
    """
    if env == ".env":
        raise BaseEnvCannotBeDeleted()

    project_meta = project.read()
    project_dir = Path(project_meta.project_dir)
    for i in project_dir.iterdir():
        if env == i.name:
            i.unlink()
            return GenericResponse(detail="success")

    raise EnvNotFound()


@router.post("/env/use", response_model=GenericResponse[str])
async def _use_project_env(
    env: str, project: NoneBotProjectManager = Depends(get_nonebot_project_manager)
) -> GenericResponse[str]:
    """
    - 切换 NoneBot 实例所应用的环境文件
    """
    project_meta = project.read()
    project_dir = Path(project_meta.project_dir)
    for i in project_dir.iterdir():
        if env == i.name:
            project.write_to_env(".env", "ENVIRONMENT", env.replace(".env", str()))
            return GenericResponse(detail="success")

    raise EnvNotFound()


@router.get("/meta/detail", response_model=ModuleConfigResponse)
async def _get_project_meta_config(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> ModuleConfigResponse:
    """
    - 获取 NoneBot 实例配置信息
    """
    project_meta = project.read()
    config_props = NoneBotProjectMeta.schema()["properties"]
    cache_list: List[ModuleConfigChild] = list()
    for prop in config_props:
        if prop not in project.meta_modifiable_keys:
            continue

        prop_detail = config_props[prop]
        item_type = prop_detail.get("type", "string")

        detail = ModuleConfigChild(
            title=prop_detail["title"],
            description=str(),
            name=prop,
            default=str(),
            item_type=item_type,
            enum=prop_detail.get("enum", list()),
            configured=getattr(project_meta, prop),
        )
        cache_list.append(detail)

    result = ModuleConfigFather(
        title="Project Config",
        description="",
        name="project-meta",
        properties=cache_list,
    )

    return ModuleConfigResponse(detail=[result])


@router.get("/nonebot/detail", response_model=ModuleConfigResponse)
async def _get_project_nonebot_config(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> ModuleConfigResponse:
    """
    - 获取 NoneBot 实例中 NoneBot 配置信息
    """
    project_meta = project.read()
    try:
        config_detail = await get_nonebot_config_detail(
            Path(project_meta.project_dir), project.config_manager.python_path
        )
    except Exception as err:
        log.error(f"Get nonebot config detail failed: {err}")
        log.exception(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 NoneBot 配置信息失败: {err}",
        )

    config_props = config_detail["properties"]
    cache_list: List[ModuleConfigChild] = list()
    for prop in config_props:
        prop_detail = config_props[prop]
        default_param = prop_detail["default"]
        default_item = (
            [str(i) for i in default_param]
            if type(default_param) in {list, set}
            else default_param
        )
        item_type = prop_detail.get("type", "string")

        detail = ModuleConfigChild(
            title=prop_detail["title"],
            description=prop_detail.get("description", str()),
            name=prop,
            default=default_item,
            item_type=item_type,
            enum=list(),
            configured=prop_detail.get("configured", str()),
        )
        cache_list.append(detail)

    result = ModuleConfigFather(
        title="NoneBot Config",
        description=config_detail.get("description", str()),
        name="nonebot-config",
        properties=cache_list,
    )

    return ModuleConfigResponse(detail=[result])


@router.get("/nonebot/plugins/detail", response_model=ModuleConfigResponse)
async def _get_project_nonebot_plugin_config(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> ModuleConfigResponse:
    """
    - 获取 NoneBot 实例中所有 NoneBot 插件设置信息
    """
    project_meta = project.read()
    plugin_list = project_meta.plugins
    result: List[ModuleConfigFather] = list()
    for plugin in plugin_list:
        config_detail = plugin.config_detail
        props = config_detail.get("properties")
        if props is None:
            continue

        cache_list: List[ModuleConfigChild] = list()
        for prop in props:
            prop_detail = props[prop]
            item_type = prop_detail.get("type", "string")
            if item_type == "object":
                configured = str(prop_detail.get("configured", str()))
                default_param = configured
            else:
                configured = prop_detail.get("configured", str())
                default_param = prop_detail.get("default", str())

            default_value = (
                [str(i) for i in default_param]
                if type(default_param) in {list, set}
                else default_param
            )

            enum = list()
            items = prop_detail.get("items")
            if items and item_type == "array":
                enum = items.get("enum", list())

            detail = ModuleConfigChild(
                title=prop_detail["title"],
                description=prop_detail.get("description", str()),
                name=prop,
                default=default_value,
                item_type=item_type,
                enum=enum,
                configured=configured,
                latest_change=prop_detail.get("latest_change", str()),
            )
            cache_list.append(detail)

        plugin_detail = ModuleConfigFather(
            title=plugin.module_name,
            description=plugin.desc,
            name=plugin.module_name,
            properties=cache_list,
        )
        result.append(plugin_detail)

    return ModuleConfigResponse(detail=result)


@router.post("/update", response_model=GenericResponse[str])
async def _update_project_config(
    module_type: str,
    data: ModuleConfigUpdateRequest,
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[str]:
    """
    - 根据模块类型及环境更新配置信息
    """

    project_meta = project.read()
    target_config = data.k.split(":")[-1]

    if module_type == "project":
        if data.key_type == "boolean":
            setattr(data, "v", bool(data.v))
        project.modify_meta(target_config, data.v)
        return GenericResponse(detail="success")

    def modify_config():
        data.v = str(data.v)
        if data.key_type in {"object", "array", "boolean"}:
            data.v = ast.literal_eval(data.v)
            v = json.dumps(data.v)
        else:
            v = data.v
        project.write_to_env(data.env, target_config, v)

        if module_type == "nonebot_plugin":
            plugins = project_meta.plugins
            for plugin in plugins:
                config_detail = plugin.config_detail
                props = config_detail.get("properties")
                if props is None:
                    continue
                for prop in props:
                    if target_config != prop:
                        continue
                    conf = props[prop].get("configured")
                    if conf is None:
                        raise ConfigNotFound()
                    plugin.config_detail["properties"][prop]["configured"] = data.v
                    plugin.config_detail["properties"][prop]["latest_change"] = data.env
                    project_meta.plugins = plugins
                    project.store(project_meta)

    project_dir = Path(project_meta.project_dir)
    for f in project_dir.iterdir():
        if data.env == f.name:
            modify_config()
            return GenericResponse(detail="success")

    raise EnvNotFound()
