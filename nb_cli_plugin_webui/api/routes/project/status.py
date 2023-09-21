import asyncio

from fastapi.websockets import WebSocketState
from fastapi import APIRouter, WebSocket, HTTPException, status

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.models.schemas.process import ProcessInfo
from nb_cli_plugin_webui.api.dependencies.process.manager import ProcessManager

router = APIRouter()


@router.get("/", response_model=ProcessInfo)
async def get_nonebot_project_process_status(project_id: str) -> ProcessInfo:
    process = ProcessManager.get_process(project_id)
    if process is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无法找到实例进程")

    return process.get_status()


@router.websocket("/{project_id}")
async def get_nonebot_project_process_status_realtime(
    websocket: WebSocket, project_id: str
) -> None:
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

    process = ProcessManager.get_process(project_id)
    if process is None:
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
    except Exception:
        pass
    return
