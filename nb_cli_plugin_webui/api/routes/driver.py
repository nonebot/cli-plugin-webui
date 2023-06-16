from fastapi import APIRouter
from nb_cli.handlers.driver import list_drivers

from nb_cli_plugin_webui.models.schemas.driver import DriverInResponse

router = APIRouter()


@router.get("/list", response_model=DriverInResponse)
async def get_driver_list() -> DriverInResponse:
    return DriverInResponse(drivers=await list_drivers())
