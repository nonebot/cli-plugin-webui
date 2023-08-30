import shutil
from pathlib import Path

from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.api.dependencies.files import BASE_DIR, get_files
from nb_cli_plugin_webui.models.schemas.files import FileMeta, FilesInResponse

router = APIRouter()


@router.get("/list", response_model=FilesInResponse)
async def get_file_list(path: str) -> FilesInResponse:
    try:
        data = get_files(BASE_DIR / Path(path))
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未找到文件")

    return FilesInResponse(files=data)


@router.post("/create", response_model=FilesInResponse)
async def create_file(
    file_data: FileMeta = Body(embed=True),
) -> FilesInResponse:
    path = BASE_DIR / Path(file_data.path) / file_data.name
    if file_data.is_dir:
        path.mkdir(exist_ok=True)
    else:
        ...
    data = get_files(Path(file_data.path))
    return FilesInResponse(files=data)


@router.delete("/delete", response_model=FilesInResponse)
async def delete_file(file_data: FileMeta) -> FilesInResponse:
    path = BASE_DIR / Path(file_data.path)
    if file_data.is_dir:
        shutil.rmtree(path)
    else:
        path.unlink()
    data = get_files(Path(file_data.path).parent)
    return FilesInResponse(files=data)
