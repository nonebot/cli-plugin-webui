import asyncio
from typing import List

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


@router.websocket("/status/{process_id}/ws")
async def _get_process_status(websocket: WebSocket, process_id: str) -> None:
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
        process: Processor = get_process(process_id)
    except Exception:
        try:
            await websocket.close()
        except Exception:
            pass
        return

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            data = process.get_status()
            await websocket.send_json(data.dict())
            await asyncio.sleep(1)
    except Exception as err:
        logger.debug(f"Process Status: {process_id=} websocket exception {err=}")
    return


@router.get("/log/history", response_model=GenericResponse[List[ProcessLog]])
async def get_log_history(
    log_id: str, log_count: int
) -> GenericResponse[List[ProcessLog]]:
    """
    - 获取历史进程日志
    """
    try:
        log_storage: LogStorage[ProcessLog] = get_log_storage(log_id)
    except LogStorageNotFound:
        raise LogStorageNotFound()

    result = log_storage.get_logs(count=log_count)
    return GenericResponse(detail=result)


@router.websocket("/log/{log_id}/ws")
async def get_process_log(
    websocket: WebSocket,
    log_id: str,
) -> None:
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
        log_storage: LogStorage[ProcessLog] = get_log_storage(log_id)
    except LogStorageNotFound:
        try:
            await websocket.close()
        except Exception:
            pass
        return

    async def log_listener(log: ProcessLog):
        await websocket.send_text(log.json())

    log_storage.register_listener(log_listener)
    logger.debug(f"Process Log: {log_id=} register listener")

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            msg = await websocket.receive()
            logger.debug(f"Process Log: websocket receive msg: {msg}")
    except Exception as err:
        logger.debug(f"Process Log: {log_id=} websocket exception {err=}")
    finally:
        log_storage.unregister_listener(log_listener)
        logger.debug(f"Process Log: {log_id=} unregister listener")
    return
