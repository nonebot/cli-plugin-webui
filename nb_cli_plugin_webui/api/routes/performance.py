import asyncio

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketState

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.api.dependencies.performance import get_system_stats
from nb_cli_plugin_webui.models.schemas.performance import SystemStatsResponse

router = APIRouter()


@router.websocket("/ws")
async def _(websocket: WebSocket):
    await websocket.accept()

    try:
        recv = await asyncio.wait_for(websocket.receive(), 5)
        token = recv.get("text", "unknown")
        jwt.verify_and_read_jwt(token, config.read().secret_key.get_secret_value())
    except Exception:
        try:
            await websocket.close()
        except Exception:
            pass
        return

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            data = await get_system_stats()
            await websocket.send_json(SystemStatsResponse(system_stats=data).dict())
            await asyncio.sleep(1)
    except Exception:
        pass
    return
