import asyncio
from typing import Tuple, Iterable, Optional

from starlette.websockets import WebSocket, WebSocketState

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.exceptions import InvalidJWTTokenError


async def accept(
    self: WebSocket,
    subprotocol: Optional[str] = None,
    headers: Optional[Iterable[Tuple[bytes, bytes]]] = None,
) -> None:
    headers = headers or list()
    if self.client_state == WebSocketState.CONNECTING:
        await self.receive()
    await self.send(
        {"type": "websocket.accept", "subprotocol": subprotocol, "headers": headers}
    )

    try:
        recv = await asyncio.wait_for(self.receive(), 5)
    except asyncio.TimeoutError as err:
        await self.close(1008)
        raise err

    token = recv.get("text", "unknown")
    try:
        jwt.verify_and_read_jwt(token, config.read().secret_key.get_secret_value())
    except Exception:
        await self.close(1008)
        raise InvalidJWTTokenError


WebSocket.accept = accept
