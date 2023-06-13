import asyncio

from fastapi import Depends, APIRouter
from fastapi.websockets import WebSocket, WebSocketState

from nb_cli_plugin_webui.api.dependencies.performance import get_system_stats
from nb_cli_plugin_webui.api.dependencies.authentication import ws_validate_key
from nb_cli_plugin_webui.models.schemas.performance import (
    SystemStats,
    SystemStatsResponse,
)

router = APIRouter()


@router.websocket("/ws")
async def _(websocket: WebSocket, data: SystemStats = Depends(get_system_stats)):
    await ws_validate_key(websocket)
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(SystemStatsResponse(system_stats=data).dict())
            await asyncio.sleep(3)
    except Exception:
        await websocket.close()
