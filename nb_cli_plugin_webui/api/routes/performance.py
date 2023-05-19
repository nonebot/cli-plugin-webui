import asyncio

from fastapi import Depends, APIRouter, status
from fastapi.websockets import WebSocket, WebSocketState

from nb_cli_plugin_webui.core.config import config
from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.models.app.performance import SystemStats
from nb_cli_plugin_webui.api.dependencies.performance import get_system_stats
from nb_cli_plugin_webui.models.schemas.performance import SystemStatsResponse

router = APIRouter()


@router.websocket("/ws")
async def _(websocket: WebSocket, data: SystemStats = Depends(get_system_stats)):
    authorization_header = websocket.headers.get("Authorization", str())
    parse_auth_header = authorization_header.split(" ")
    if not parse_auth_header or len(parse_auth_header) != 2:
        await websocket.close(status.WS_1003_UNSUPPORTED_DATA)
        return
    else:
        token = parse_auth_header[1]
        try:
            jwt.verify_and_read_jwt(token, config.read().secret_key.get_secret_value())
        except Exception:
            await websocket.close(status.WS_1008_POLICY_VIOLATION)
            return

    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(SystemStatsResponse(system_stats=data).dict())
            await asyncio.sleep(3)
    except Exception:
        await websocket.close()
