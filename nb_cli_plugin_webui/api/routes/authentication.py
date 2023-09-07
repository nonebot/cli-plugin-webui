from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.models.schemas.authentication import (
    LoginData,
    LoginResponse,
    IsAvailableResponse,
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginData = Body(embed=True),
) -> LoginResponse:
    if not login_data.check_token():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="密钥不可用")

    jwt_token = jwt.create_access_for_header(
        login_data.mark, config.read().secret_key.get_secret_value()
    )
    return LoginResponse(jwt_token=jwt_token)


@router.get("/is_available", response_model=IsAvailableResponse)
async def is_alive() -> IsAvailableResponse:
    return IsAvailableResponse(detail="0w0")
