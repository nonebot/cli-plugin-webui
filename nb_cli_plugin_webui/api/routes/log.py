from fastapi import APIRouter, status
from fastapi.websockets import WebSocket, WebSocketState, WebSocketDisconnect

from nb_cli_plugin_webui.models.domain.process import ProcessLog
from nb_cli_plugin_webui.api.dependencies.authentication import ws_validate_key
from nb_cli_plugin_webui.api.dependencies.process.log import LoggerStorageFather

router = APIRouter()


@router.websocket("/logs/{log_key}")
async def _(websocket: WebSocket, log_key: str):
    await ws_validate_key(websocket)

    log = LoggerStorageFather[ProcessLog].get_storage(log_key)
    if log is None:
        await websocket.close(status.WS_1003_UNSUPPORTED_DATA)
        return

    async def log_listener(log: ProcessLog):
        await websocket.send_json(log.dict())

    log.register_listener(log_listener)

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            _ = await websocket.receive()
    except WebSocketDisconnect:
        pass
    finally:
        log.unregister_listener(log_listener)
