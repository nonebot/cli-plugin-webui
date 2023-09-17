import shutil
from pathlib import Path

from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.api.dependencies.files import BASE_DIR, get_files
from nb_cli_plugin_webui.models.schemas.files import FileMeta, FilesInResponse

router = APIRouter()


@router.get("/list", response_model=FilesInResponse)
async def get_file_list(path: str) -> FilesInResponse:
    try:
        data = get_files(BASE_DIR / Path(path), BASE_DIR)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未找到文件")

    return FilesInResponse(files=data)


@router.post("/create", response_model=FilesInResponse)
async def create_file(
    file_data: FileMeta = Body(embed=True),
) -> FilesInResponse:
    working_dir = BASE_DIR / Path(file_data.path)
    path = working_dir / file_data.name
    if file_data.is_dir:
        path.mkdir(exist_ok=True)
    else:
        with open(path, "w", encoding="utf-8") as w:
            w.write(str())
    data = get_files(working_dir, BASE_DIR)
    return FilesInResponse(files=data)


@router.delete("/delete", response_model=FilesInResponse)
async def delete_file(path: str) -> FilesInResponse:
    working_dir = BASE_DIR / Path(path)
    if not working_dir.exists():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件不存在")

    try:
        shutil.rmtree(working_dir)
    except OSError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"删除文件失败 {err=}"
        )
    data = get_files(working_dir.parent, BASE_DIR)
    return FilesInResponse(files=data)
