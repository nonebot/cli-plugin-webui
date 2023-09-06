class TokenComplexityError(Exception):
    """token complexity error."""


class InvalidJWTTokenError(Exception):
    """invalid jwt token error."""


class ConfigIsNotExist(Exception):
    """config file is not exist."""


class ProcessAlreadyRunning(Exception):
    """target process already running."""


class ProcessAlreadyExist(Exception):
    """target process already exist."""


class LoggerStorageAlreadyExist(Exception):
    """target log storage already exist."""


class FunctionAlreadyExist(Exception):
    """target function already exist."""


class NonebotProjectIsNotExist(Exception):
    """target nonebot project is not exist."""


class InvalidKeyException(Exception):
    """invalid key is provided."""
