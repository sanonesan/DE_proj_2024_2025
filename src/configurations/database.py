"""
Configuration for database connections
"""
from typing import AsyncGenerator, Optional

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)


from src.logs.console_logger import LOGGER
from src.configurations.settings import SETTINGS


__async_engine_ds: Optional[AsyncEngine] = None
__async_engine_logger: Optional[Engine] = None


def global_init() -> None:
    """
    Initializes global asynchronous database connection engines and the database logger.

    This function creates and stores:
    - `__async_engine_ds`: An async engine for the main data source
        (using `SETTINGS.ds_database_url`).
    - `__async_engine_logger`: An async engine for the main data source
        (using `SETTINGS.logger_database_url`).


    Engines are created only if they don't exist. Initialization logs are also generated.
    """

    global __async_engine_ds, __async_engine_logger # pylint: disable=global-statement

    if not __async_engine_logger:

        __async_engine_logger = create_async_engine(
            url=SETTINGS.logger_database_url,
            echo=False,
        )

        LOGGER.info(msg="INIT __async_engine_logger")

    if not __async_engine_ds:
        __async_engine_ds = create_async_engine(
            url=SETTINGS.ds_database_url,
            echo=False,
        )
        LOGGER.info(msg="INIT __async_engine_ds")


async def async_ds_db_connection() -> AsyncGenerator:
    """
    Yield connection to DS schema in database
    """
    async with __async_engine_ds.connect() as conn:
        yield conn


async def async_logger_db_connection() -> AsyncGenerator:
    """
    Yield connection to LOGS schema in database
    """
    async with __async_engine_logger.connect() as conn:
        yield conn
