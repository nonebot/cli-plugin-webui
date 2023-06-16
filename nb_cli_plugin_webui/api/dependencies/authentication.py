import asyncio
from typing import List, Optional

from fastapi import status
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Send, Scope, ASGIApp, Receive
from fastapi.security.utils import get_authorization_scheme_param

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config


class CustomAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        pass_paths: Optional[List[str]] = None,
    ) -> None:
        super().__init__(app)
        self.pass_paths = pass_paths or list()

    async def _ws_close(
        self, send: Send, code: int = 1000, reason: Optional[str] = None
    ) -> None:
        if reason is None:
            reason = str()
        await send({"type": "websocket.close", "code": code, "reason": reason})

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "websocket":
            await receive()
            try:
                recv = await asyncio.wait_for(receive(), 5)
            except asyncio.TimeoutError:
                await self._ws_close(send, 1008)
                return

            token = recv.get("text", "unknown")
            try:
                jwt.verify_and_read_jwt(
                    token, config.read().secret_key.get_secret_value()
                )
            except Exception:
                await self._ws_close(send, 1008)
                return
        else:
            await self.app(scope, receive, send)

    def get_current_header(
        self,
        request: Request,
    ) -> None:
        authorization = request.headers.get("Authorization")
        _, param = get_authorization_scheme_param(authorization)
        jwt.verify_and_read_jwt(param, config.read().secret_key.get_secret_value())

    async def dispatch(self, request, call_next) -> Response:
        path = request.url.path
        for p in self.pass_paths:
            if p in path:
                response = await call_next(request)
                return response

        try:
            self.get_current_header(request)
            response = await call_next(request)
            return response
        except Exception as err:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(err)}
            )
