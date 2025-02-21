from typing import Callable

from fastapi import FastAPI

from src.conf.settings.app import AppSettings
from src.models.db_init import init as init_db


def create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        init_db()

    return start_app


# def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
#     @logger.catch
#     async def stop_app() -> None:
#         await close_db_connection(app)

#     return stop_app
