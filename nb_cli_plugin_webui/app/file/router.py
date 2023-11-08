import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.logging import logger as log

from .utils import list_file
from .schemas import SimpleModel, FileResponse
from .exceptions import PathIsNotDir, PathIsNotExists

router = APIRouter()


@router.get("/list", response_model=FileResponse)
async def get_file_list(path: str) -> FileResponse:
    """
    - 根据提供的路径, 基于 base_dir 返回文件列表
    """
    working_dir = Config.base_dir / Path(path)
    if not working_dir.exists():
        raise PathIsNotExists()
    if not working_dir.is_dir():
        raise PathIsNotDir()
    result = list_file(working_dir, Path(Config.base_dir))
    return FileResponse(detail=result)


@router.post("/create", response_model=FileResponse)
async def create_file(data: SimpleModel) -> FileResponse:
    """
    - 根据提供的路径, 基于 base_dir 创建文件
    """
    working_dir = Config.base_dir / Path(data.path)
    path = working_dir / data.name
    if data.is_dir:
        path.mkdir(exist_ok=True)
    else:
        path.write_text(str(), encoding="utf-8")
    result = list_file(working_dir, Path(Config.base_dir))
    return FileResponse(detail=result)


@router.delete("/delete", response_model=FileResponse)
async def delete_file(path: str) -> FileResponse:
    """
    - 根据提供的路径, 基于 base_dir 删除文件
    """
    working_dir = Config.base_dir / Path(path)
    if not working_dir.exists():
        raise PathIsNotExists()

    try:
        shutil.rmtree(working_dir)
    except OSError as err:
        log.error(f"Delete file failed: {err}")
        log.exception(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"删除文件失败 {err=}"
        )

    result = list_file(working_dir.parent, Path(Config.base_dir))
    return FileResponse(detail=result)
