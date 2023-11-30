from typing import Dict, List, Callable, Optional, Awaitable

from fastapi.websockets import WebSocketState
from fastapi import Depends, APIRouter, WebSocket

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.logging import logger
from nb_cli_plugin_webui.app.schemas import GenericResponse
from nb_cli_plugin_webui.app.auth.utils import websocket_auth
from nb_cli_plugin_webui.app.project import (
    NoneBotProjectManager,
    get_nonebot_project_manager,
)
from nb_cli_plugin_webui.app.handlers.process import (
    Processor,
    LogStorage,
    ProcessLog,
    LogStorageNotFound,
)

from .service import run_nonebot_project
from .dependencies import get_process, get_log_storage
from .exceptions import DriverNotFound, AdapterNotFound

router = APIRouter()
log_storage: Optional[LogStorage[ProcessLog]] = None
log_listeners: Dict[WebSocket, Callable[[ProcessLog], Awaitable[None]]] = dict()


@router.post("/run", response_model=GenericResponse[str])
async def run_process(
    project: NoneBotProjectManager = Depends(get_nonebot_project_manager),
) -> GenericResponse[str]:
    """
    - 运行 NoneBot 实例
    """
    project_meta = project.read()
    if not project_meta.adapters:
        raise AdapterNotFound()
    if not project_meta.drivers:
        raise DriverNotFound()

    await run_nonebot_project(project)
    return GenericResponse(detail="success")


@router.post("/stop", response_model=GenericResponse[str])
async def _stop_process(
    process: Processor = Depends(get_process),
) -> GenericResponse[str]:
    """
    - 终止 NoneBot 实例
    """
    await process.stop()
    return GenericResponse(detail="success")


@router.post("/write", response_model=GenericResponse[int])
async def write_to_process(
    content: str,
    process: Processor = Depends(get_process),
) -> GenericResponse[int]:
    """
    - 向 NoneBot 实例进程写入数据
    """
    result = await process.write_stdin(content.encode())
    return GenericResponse(detail=result)


@router.get("/log/history", response_model=GenericResponse[List[ProcessLog]])
async def get_log_history(
    log_count: int, log_storage: LogStorage = Depends(get_log_storage)
) -> GenericResponse[List[ProcessLog]]:
    """
    - 获取历史进程日志
    """
    result = log_storage.get_logs(count=log_count)
    return GenericResponse(detail=result)


@router.websocket("/log/ws")
async def get_process_log(websocket: WebSocket):
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

    def unregister_listener(log_storage: LogStorage[ProcessLog]):
        listener = log_listeners.get(websocket)
        if listener is not None:
            log_storage.unregister_listener(listener)
            log_listeners.pop(websocket)

    async def log_listener(log: ProcessLog):
        await websocket.send_text(log.json())

    async def receive_listener(recv: dict):
        global log_storage

        if log_storage is not None:
            unregister_listener(log_storage)

        if recv.get("type") != "log":
            return

        log_key = recv.get("log_key", str())
        try:
            log_storage = get_log_storage(log_key)
        except LogStorageNotFound:
            return

        log_storage.register_listener(log_listener)
        log_listeners[websocket] = log_listener

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            recv = await websocket.receive_json()
            await receive_listener(recv)
    except Exception as err:
        logger.debug(f"Process Log: websocket exception {err=}")
    finally:
        if log_storage is not None:
            unregister_listener(log_storage)
