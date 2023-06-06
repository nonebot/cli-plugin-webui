import shutil
from pathlib import Path

from fastapi import Body, Depends, APIRouter, HTTPException, status

from nb_cli_plugin_webui.api.dependencies.files import BASE_DIR, get_files
from nb_cli_plugin_webui.api.dependencies.authentication import get_current_header
from nb_cli_plugin_webui.models.schemas.files import (
    FileListRequest,
    FilesInResponse,
    FileOperateRequest,
)

router = APIRouter(dependencies=[Depends(get_current_header)])


@router.post("/list", response_model=FilesInResponse)
async def get_file_list(
    path_data: FileListRequest = Body(embed=True),
) -> FilesInResponse:
    try:
        data = get_files(BASE_DIR / Path(path_data.path))
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return FilesInResponse(files=data)


@router.post("/create", response_model=FilesInResponse)
async def create_file(
    file_data: FileOperateRequest = Body(embed=True),
) -> FilesInResponse:
    path = BASE_DIR / Path(file_data.path) / file_data.file_name
    if file_data.is_dir:
        path.mkdir(exist_ok=True)
    else:
        ...
    data = get_files(Path(file_data.path))
    return FilesInResponse(files=data)


@router.post("/delete", response_model=FilesInResponse)
async def delete_file(
    file_data: FileOperateRequest = Body(embed=True),
) -> FilesInResponse:
    path = BASE_DIR / Path(file_data.path)
    if file_data.is_dir:
        shutil.rmtree(path)
    else:
        path.unlink()
    data = get_files(Path(file_data.path).parent)
    return FilesInResponse(files=data)
