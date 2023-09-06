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
        pass_paths: Optional[List[str]] = None,
    ) -> None:
        super().__init__(app)
        self.pass_paths = pass_paths or list()

    async def dispatch(self, request, call_next) -> Response:
        path = request.url.path
        for p in self.pass_paths:
            if "*" in p:
                pass_key_path = p.split("/")[1]
                check_key_path = path.split("/")[1]
                if pass_key_path == check_key_path:
                    response = await call_next(request)
                    return response

            if p == path:
                response = await call_next(request)
                return response

        authorization = request.headers.get("Authorization")
        _, param = get_authorization_scheme_param(authorization)
        try:
            jwt.verify_and_read_jwt(param, config.read().secret_key.get_secret_value())
            response = await call_next(request)
            return response
        except Exception as err:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(err)}
            )
