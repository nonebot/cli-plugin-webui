from fastapi import APIRouter
from fastapi.websockets import WebSocketState, WebSocketDisconnect

from nb_cli_plugin_webui.patch import WebSocket
from nb_cli_plugin_webui.models.domain.process import ProcessLog
from nb_cli_plugin_webui.api.dependencies.process.log import LoggerStorageFather

router = APIRouter()


@router.websocket("/logs/{log_key}")
async def _(websocket: WebSocket, log_key: str):
    await websocket.accept()

    log = LoggerStorageFather[ProcessLog].get_storage(log_key)
    if log is None:
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
    return
