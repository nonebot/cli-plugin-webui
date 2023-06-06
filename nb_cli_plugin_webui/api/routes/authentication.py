from fastapi import Body, Depends, APIRouter, HTTPException, status

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.models.schemas.user import UserInLogin, UserInResponse
from nb_cli_plugin_webui.models.schemas.authentication import IsAvailableResponse
from nb_cli_plugin_webui.api.dependencies.authentication import get_current_header

router = APIRouter()


@router.post("/login", response_model=UserInResponse)
async def login(
    login_data: UserInLogin = Body(embed=True),
) -> UserInResponse:
    if not login_data.check_token():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    jwt_token = jwt.create_access_for_header(
        login_data.mark, config.read().secret_key.get_secret_value()
    )
    return UserInResponse(jwt_token=jwt_token)


@router.get("/is_available", response_model=IsAvailableResponse)
async def is_alive(_=Depends(get_current_header)) -> IsAvailableResponse:
    return IsAvailableResponse(detail="0w0")
