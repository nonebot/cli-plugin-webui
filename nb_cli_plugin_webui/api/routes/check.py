from pathlib import Path

from fastapi import APIRouter

from nb_cli_plugin_webui.models.schemas.check import PathCheckInResponse

router = APIRouter()


@router.post("/path", response_model=PathCheckInResponse)
async def check_path(path: str) -> PathCheckInResponse:
    return (
        PathCheckInResponse(is_exist=1)
        if Path(path).exists()
        else PathCheckInResponse(is_exist=0)
    )
