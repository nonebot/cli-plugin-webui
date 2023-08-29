from fastapi import APIRouter
from fastapi.websockets import WebSocketState, WebSocketDisconnect

from nb_cli_plugin_webui.patch import WebSocket
from nb_cli_plugin_webui.models.domain.process import ProcessLog
from nb_cli_plugin_webui.models.schemas.log import LogHistoryResponse
from nb_cli_plugin_webui.api.dependencies.process.log import LoggerStorageFather

router = APIRouter()


@router.get("/logs/history", response_model=LogHistoryResponse)
async def get_logs_history(log_key: str, log_count: int = 0) -> LogHistoryResponse:
    log = LoggerStorageFather[ProcessLog].get_storage(log_key)
    result = list()
    if log:
        result = result = log.get_logs(limit=log_count, is_dict=True)

    return LogHistoryResponse(detail=result)


@router.websocket("/logs/{log_key}")
async def get_logs_realtime(websocket: WebSocket, log_key: str):
    await websocket.accept()

    log = LoggerStorageFather[ProcessLog].get_storage(log_key)
    if log is None:
        await websocket.close()
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
