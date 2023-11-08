from typing import Any

from fastapi import HTTPException, status


class BaseServerException(HTTPException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.code, detail=self.detail, **kwargs)


class PermissionDenied(BaseServerException):
    code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"


class NotFound(BaseServerException):
    code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class BadRequest(BaseServerException):
    code = status.HTTP_400_BAD_REQUEST
    detail = "Bad request"


class NotAuthenticated(BaseServerException):
    code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated"


class RateLimited(BaseServerException):
    code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Rate limited"
