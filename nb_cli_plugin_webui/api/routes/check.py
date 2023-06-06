from pathlib import Path

from fastapi import Body, Depends, APIRouter

from nb_cli_plugin_webui.models.schemas.check import PathInCheck, PathInResponse
from nb_cli_plugin_webui.api.dependencies.authentication import get_current_header

router = APIRouter(dependencies=[Depends(get_current_header)])


@router.post("/path", response_model=PathInResponse)
async def check_path(path_data: PathInCheck = Body(embed=True)) -> PathInResponse:
    path = Path(path_data.path)
    return PathInResponse(is_exist=1) if path.exists() else PathInResponse(is_exist=0)
