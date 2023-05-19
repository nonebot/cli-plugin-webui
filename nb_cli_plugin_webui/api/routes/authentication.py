from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.core.config import config
from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.models.schemas.user import (
    UserInLogin,
    UserWithJWT,
    UserInResponse,
)

router = APIRouter()


@router.post("/login", response_model=UserInResponse)
async def login(
    login_data: UserInLogin = Body(..., embed=True),
) -> UserInResponse:
    if not login_data.check_token():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    jwt_token = jwt.create_access_for_cookie(
        login_data.string, config.read().secret_key.get_secret_value()
    )
    return UserInResponse(user=UserWithJWT(jwt_token=jwt_token))
