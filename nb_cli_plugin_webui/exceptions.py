class TokenComplexityError(Exception):
    """token complexity error."""


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


class NonebotProjectFileIsNotExist(Exception):
    """nonebot projects info file is not exist."""


class NonebotProjectIsNotExist(Exception):
    """target nonebot project is not exist."""
