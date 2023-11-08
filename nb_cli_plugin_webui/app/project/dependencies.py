from pathlib import Path

from fastapi import HTTPException, status
from nb_cli.exceptions import ProjectNotFoundError

from nb_cli_plugin_webui.app.logging import logger as log
from nb_cli_plugin_webui.app.handlers import NoneBotProjectManager

from .schemas import ProjectTomlDetail
from .utils import get_nonebot_info_from_toml
from .exceptions import ProjectTomlNotFound, NoneBotProjectNotFound


def get_nonebot_project_manager(project_id: str) -> NoneBotProjectManager:
    project = NoneBotProjectManager(project_id=project_id)
    try:
        project.read()
    except ProjectNotFoundError:
        raise NoneBotProjectNotFound()
    return project


def get_nonebot_project_toml(project_dir: str) -> ProjectTomlDetail:
    path = Path(project_dir)
    try:
        toml_data = get_nonebot_info_from_toml(path)
    except FileNotFoundError:
        raise ProjectTomlNotFound()
    except Exception as err:
        log.error("Get nonebot project toml failed.")
        log.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"其它未知错误：{err}"
        )
    return toml_data
