from fastapi import APIRouter
from nb_cli.handlers.adapter import list_adapters

from nb_cli_plugin_webui.models.schemas.adapter import AdapterInResponse

router = APIRouter()


@router.get("/list", response_model=AdapterInResponse)
async def get_adapter_list() -> AdapterInResponse:
    return AdapterInResponse(adapters=await list_adapters())
