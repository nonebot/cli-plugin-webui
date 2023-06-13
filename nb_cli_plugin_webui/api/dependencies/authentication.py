from fastapi import Depends, WebSocket, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from nb_cli_plugin_webui.utils.security import jwt
from nb_cli_plugin_webui.core.configs.config import config

security = HTTPBearer()


def get_current_header(
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


async def ws_validate_key(websocket: WebSocket):
    await websocket.accept()
    token = await websocket.receive_text()

    try:
        jwt.verify_and_read_jwt(token, config.read().secret_key.get_secret_value())
    except Exception:
        await websocket.close(status.WS_1008_POLICY_VIOLATION)
        return
