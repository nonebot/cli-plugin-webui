import asyncio
from typing import Optional

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from nb_cli_plugin_webui.exceptions import InvalidJWTTokenError


def add_exception_handler(app: FastAPI) -> FastAPI:
    app.add_exception_handler(Exception, handle_custom_exception)
    app.add_exception_handler(asyncio.TimeoutError, handle_custom_exception)
    app.add_exception_handler(InvalidJWTTokenError, handle_invalid_jwt_token_exception)
    return app


async def handle_custom_exception(
    request: Request, exc: Optional[Exception]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


async def handle_invalid_jwt_token_exception(
    request: Request, exc: InvalidJWTTokenError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)}
    )
