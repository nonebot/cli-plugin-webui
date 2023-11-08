import asyncio

from fastapi import WebSocket

from nb_cli_plugin_webui.app.utils.security import jwt


async def websocket_auth(websocket: WebSocket, *, secret_key: str) -> bool:
    try:
        recv = await asyncio.wait_for(websocket.receive(), 5)
        token = recv.get("text", "unknown")
        jwt.verify_and_read_jwt(token, secret_key)
    except Exception:
        return False
    return True
