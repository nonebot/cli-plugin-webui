import asyncio
from typing import Optional

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketState

from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.auth.utils import websocket_auth
from nb_cli_plugin_webui.app.handlers.process import Processor
from nb_cli_plugin_webui.app.process.dependencies import get_process

from . import utils
from .schemas import StatusInfo, SystemInfo

router = APIRouter()


@router.websocket("/ws")
async def get_performance(websocket: WebSocket) -> None:
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

    process: Optional[Processor] = None
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            try:
                receive_task = asyncio.create_task(websocket.receive_json())
                send_task = asyncio.create_task(send_status_info(websocket, process))

                done, pending = await asyncio.wait(
                    [receive_task, send_task], return_when=asyncio.FIRST_COMPLETED
                )

                for task in pending:
                    task.cancel()

                for task in done:
                    if task == receive_task:
                        try:
                            msg = receive_task.result()
                            if msg.get("type") == "status":
                                project_id = msg.get("project_id")
                                process = get_process(project_id)
                        except Exception:
                            pass
            except Exception:
                pass

            await asyncio.sleep(1)
    except Exception:
        pass
    return


async def send_status_info(websocket: WebSocket, process: Optional[Processor]) -> None:
    await websocket.send_json(
        StatusInfo(
            system=SystemInfo(
                platform=utils.get_platform_info(),
                cpu=await utils.get_cpu_info(),
                mem=utils.get_mem_info(),
                disk=utils.get_disk_info(),
                net=utils.get_net_info(),
            ),
            process=process.get_status() if process else None,
        ).dict()
    )
