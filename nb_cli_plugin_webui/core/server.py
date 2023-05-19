import uvicorn


async def run_server(host: str, port: int):
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "default": {
                "class": "nb_cli_plugin_webui.core.log.LoguruHandler",
            },
        },
        "loggers": {
            "uvicorn.error": {"handlers": ["default"], "level": "INFO"},
            "uvicorn.access": {
                "handlers": ["default"],
                "level": "INFO",
            },
        },
    }

    server = uvicorn.Server(
        uvicorn.Config(
            "nb_cli_plugin_webui.api:app",
            host=host,
            port=port,
            log_config=LOGGING_CONFIG,
        )
    )

    return await server.serve()
