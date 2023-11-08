import asyncio

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketState

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.auth.utils import websocket_auth

from . import utils
from .schemas import PlatformInfo

router = APIRouter()


@router.websocket("/platform/ws")
async def get_platform_performance(websocket: WebSocket) -> None:
    await websocket.accept()

    auth = await websocket_auth(
        websocket, secret_key=Config.secret_key.get_secret_value()
    )
    if not auth:
        try:
            await websocket.close()
        except Exception:
            pass
        return

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(
                PlatformInfo(
                    platform=utils.get_platform_info(),
                    cpu=await utils.get_cpu_info(),
                    mem=utils.get_mem_info(),
                    disk=utils.get_disk_info(),
                    net=utils.get_net_info(),
                ).dict()
            )
            await asyncio.sleep(1)
    except Exception:
        pass
    return
