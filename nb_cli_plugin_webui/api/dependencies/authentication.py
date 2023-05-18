from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from nb_cli_plugin_webui.config import config
from nb_cli_plugin_webui.utils.security import jwt

security = HTTPBearer()


def get_current_cookie(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    try:
        token = credentials.credentials
        result = jwt.verify_and_read_jwt(
            token, config.read().secret_key.get_secret_value()
        )
        return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials",
        )
