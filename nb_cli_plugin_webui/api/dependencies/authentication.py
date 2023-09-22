from typing import List, Optional

from fastapi import status
from starlette.types import ASGIApp
from starlette.responses import Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security.utils import get_authorization_scheme_param

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config


class CustomAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        auth_router: Optional[List[str]] = None,
        pass_paths: Optional[List[str]] = None,
    ) -> None:
        super().__init__(app)
        self.auth_router = auth_router or list()
        self.pass_paths = pass_paths or list()
        self.secret_key = config.read().secret_key.get_secret_value()

    async def dispatch(self, request, call_next) -> Response:
        request_path = request.url.path

        if request_path in self.pass_paths:
            return await call_next(request)

        authorization = request.headers.get("Authorization")
        _, param = get_authorization_scheme_param(authorization)
        if any(request_path.startswith(route) for route in self.auth_router):
            try:
                jwt.verify_and_read_jwt(param, self.secret_key)
            except Exception as err:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(err)}
                )

        return await call_next(request)
