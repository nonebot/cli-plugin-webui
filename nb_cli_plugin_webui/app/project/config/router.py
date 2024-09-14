import re
import ast
import json
from pathlib import Path
from typing import Any, Dict, List

from fastapi import Depends, APIRouter, HTTPException, status

from nb_cli_plugin_webui.app.constants import ModuleType
from nb_cli_plugin_webui.app.logging import logger as log
from nb_cli_plugin_webui.app.schemas import NoneBotProjectMeta
from nb_cli_plugin_webui.app.handlers import (
    NoneBotProjectManager,
    get_nonebot_config_detail,
)

from ..dependencies import get_nonebot_project_manager
from .exceptions import EnvExists, EnvNotFound, ConfigNotFound, BaseEnvCannotBeDeleted
from .schemas import (
    ConfigType,
    GenericResponse,
    ConfigModuleType,
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
            env_name = str()
            _match = re.compile(r"(?<=\.env\.)[\w-]+")
            search = _match.search(env)
            if search:
                env_name = search.group()

            project.write_to_env(".env", "ENVIRONMENT", env_name)
            project_meta.use_env = env
            project.store(project_meta)

            return GenericResponse(detail="success")

    raise EnvNotFound()


@router.get("/meta/detail", response_model=ModuleConfigResponse)
async def _get_project_meta_config(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> ModuleConfigResponse:
    """
    - 获取 NoneBot 实例在 .toml 中的配置信息
    """
    project_meta = project.read()
    config_props = NoneBotProjectMeta.schema()["properties"]
    cache_list: List[ModuleConfigChild] = list()
    for prop in config_props:
        if prop not in project.meta_modifiable_keys:
            continue

        prop_detail = config_props[prop]
        conf_type = prop_detail.get("type", "string")

        detail = ModuleConfigChild(
            title=prop_detail["title"],
            description=str(),
            name=prop,
            default=str(),
            conf_type=conf_type,
            enum=prop_detail.get("enum", list()),
            is_secret=prop_detail.get("writeOnly", False),
            configured=getattr(project_meta, prop),
        )
        cache_list.append(detail)

    result = ModuleConfigFather(
        title="Project Config",
        description="",
        name="project-meta",
        module_type=ConfigType.toml,
        properties=cache_list,
    )

    return ModuleConfigResponse(detail=[result])


@router.get("/nonebot/detail", response_model=ModuleConfigResponse)
async def _get_project_nonebot_config(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> ModuleConfigResponse:
    """
    - 获取 NoneBot 实例配置信息
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
        conf_type = prop_detail.get("type", "string")

        detail = ModuleConfigChild(
            title=prop_detail["title"],
            description=prop_detail.get("description", str()),
            name=prop,
            default=default_item,
            conf_type=conf_type,
            enum=prop_detail.get("enum", list()),
            is_secret=prop_detail.get("writeOnly", False),
            configured=prop_detail.get("configured", str()),
        )
        cache_list.append(detail)

    result = ModuleConfigFather(
        title="NoneBot Config",
        description=config_detail.get("description", str()),
        name="nonebot-config",
        module_type=ConfigType.project,
        properties=cache_list,
    )

    return ModuleConfigResponse(detail=[result])


@router.get("/nonebot/plugin/detail", response_model=ModuleConfigResponse)
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
            conf_type = prop_detail.get("type", "string")
            if conf_type == "object":
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
            if items and conf_type == "array":
                enum = items.get("enum", list())

            detail = ModuleConfigChild(
                title=prop_detail["title"],
                description=prop_detail.get("description", str()),
                name=prop,
                default=default_value,
                conf_type=conf_type,
                enum=enum,
                configured=configured,
                is_secret=prop_detail.get("writeOnly", False),
                latest_change=prop_detail.get("latest_change", str()),
            )
            cache_list.append(detail)

        plugin_detail = ModuleConfigFather(
            title=plugin.module_name,
            description=plugin.desc,
            name=plugin.module_name,
            module_type=ModuleType.plugin,
            properties=cache_list,
        )
        result.append(plugin_detail)

    return ModuleConfigResponse(detail=result)


@router.post("/update", response_model=GenericResponse[str])
async def _update_project_config(
    module_type: ConfigModuleType,
    data: ModuleConfigUpdateRequest,
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[str]:
    """
    - 根据模块类型及环境更新配置信息
    - 说明:
        * `module_type` 仅作 WebUI 更新自身存储的实例信息，不会影响实例本体
    """

    # TODO: 修复modify_config 中接受的 value 类型判断不准确。module_type 需重新考虑

    project_meta = project.read()
    target_config = data.k.split(":")[-1]

    if module_type == ConfigType.toml:
        if data.conf_type == "boolean":
            setattr(data, "v", bool(data.v))

        project.modify_meta(target_config, data.v)

        toml_data = project.get_toml_data()
        table: Dict[str, Any] = toml_data.setdefault("tool", {}).setdefault(
            "nonebot", {}
        )
        table[data.k] = data.v
        project.write_toml_data(toml_data)

        return GenericResponse(detail="success")

    def modify_config():
        data.v = str(data.v)
        if data.conf_type in {"object", "array", "boolean"}:
            data.v = ast.literal_eval(data.v)
            v = json.dumps(data.v)
        else:
            v = data.v
        project.write_to_env(data.env, target_config, v)

        if module_type == ModuleType.plugin:
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
