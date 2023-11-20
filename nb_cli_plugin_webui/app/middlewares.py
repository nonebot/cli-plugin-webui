from typing import Callable, Awaitable

from starlette.responses import JSONResponse
from fastapi import Request, Response, status
from starlette.middleware.cors import CORSMiddleware
from fastapi.security.utils import get_authorization_scheme_param

from .config import Config
from .application import app
from .utils.security import jwt

AUTH_ROUTES = ["/api"]
PASS_PATHS = [
    "/api/v1/auth/login",
    "/api/docs",
    "/api/docs/openapi.json",
]

RequestHandler = Callable[[Request], Awaitable[Response]]


@app.middleware("http")
async def auth(request: Request, call_next: RequestHandler) -> Response:
    request_path = request.url.path

    if request_path in PASS_PATHS:
        return await call_next(request)

    authorization = request.headers.get("Authorization")
    _, param = get_authorization_scheme_param(authorization)
    if any(request_path.startswith(route) for route in AUTH_ROUTES):
        secret_key = Config.secret_key.get_secret_value()
        try:
            jwt.verify_and_read_jwt(param, secret_key)
        except Exception as err:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(err)}
            )

    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
