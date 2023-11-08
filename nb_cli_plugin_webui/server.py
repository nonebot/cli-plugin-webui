import uvicorn

from nb_cli_plugin_webui.app.logging import LOG_LEVEL

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "nb_cli_plugin_webui.app.logging.LoguruHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
    },
}


async def run_server(host: str, port: int):
    server = uvicorn.Server(
        uvicorn.Config(
            "nb_cli_plugin_webui.app:app",
            host=host,
            port=port,
            log_config=LOG_CONFIG,
        )
    )
    return await server.serve()
