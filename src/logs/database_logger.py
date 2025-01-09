"""
    A class for asynchronous logging to a database.
"""

import datetime
from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncConnection

from src.database.schemas.logs.logs import AsyncQuerier, CreateLogParams


class AsyncDatabaseLogger:
    """
    A class for asynchronous logging to a database.
    """

    __level: str = "INFO"  # Default Level

    def __init__(self, level: str = "INFO"):
        """
        Initializes the logger instance

        Args:
                level (str, optional): Default log level. Defaults to "INFO".
        """
        self.__level = level

    async def __log(
        self,
        msg: str,
        conn: AsyncConnection,
        level: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Internal method to write a log message to the database.

        Args:
            msg (str): The log message.
            conn (AsyncConnection): Asynchronous database connection.
            level (Optional[str], optional): Log level. Defaults to None.
            extra (Dict[str, Any]): Extra parameters. Defaults to
                {"application_name": "default_name"}.
        """

        if not level:
            level = self.__level

        try:
            app_name = extra["application_name"]
        except Exception:
            app_name = "default_name"

        querier = AsyncQuerier(conn)

        await querier.create_log(
            CreateLogParams(
                application_name=app_name,
                log_level=level,
                log_timestamp=datetime.datetime.now(datetime.timezone.utc),
                log_message=msg,
            )
        )
        await conn.commit()

    @classmethod
    async def debug(
        cls,
        msg: str,
        conn: AsyncConnection,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Logs a debug message to the database.

        Args:
            msg (str): The log message.
            conn (AsyncConnection): Asynchronous database connection.
            extra (Dict[str, Any]): Extra parameters. Defaults to 
                {"application_name": "default_name"}.
        """
        level: str = "DEBUG"

        await cls.__log(
            cls,
            msg=msg,
            conn=conn,
            level=level,
            extra=extra,
        )

    @classmethod
    async def info(
        cls,
        msg: str,
        conn: AsyncConnection,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Logs a info message to the database.

        Args:
            msg (str): The log message.
            conn (AsyncConnection): Asynchronous database connection.
            extra (Dict[str, Any]): Extra parameters. Defaults to 
                {"application_name": "default_name"}.
        """
        level: str = "INFO"

        await cls.__log(
            cls,
            msg=msg,
            conn=conn,
            level=level,
            extra=extra,
        )

    @classmethod
    async def warning(
        cls,
        msg: str,
        conn: AsyncConnection,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Logs a warning message to the database.

        Args:
            msg (str): The log message.
            conn (AsyncConnection): Asynchronous database connection.
            extra (Dict[str, Any]): Extra parameters. Defaults to 
                {"application_name": "default_name"}.
        """
        level: str = "WARNING"

        await cls.__log(
            cls,
            msg=msg,
            conn=conn,
            level=level,
            extra=extra,
        )

    @classmethod
    async def error(
        cls,
        msg: str,
        conn: AsyncConnection,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Logs a error message to the database.

        Args:
            msg (str): The log message.
            conn (AsyncConnection): Asynchronous database connection.
            extra (Dict[str, Any]): Extra parameters. Defaults to 
                {"application_name": "default_name"}.
        """
        level: str = "ERROR"

        await cls.__log(
            cls,
            msg=msg,
            conn=conn,
            level=level,
            extra=extra,
        )

    @classmethod
    async def critical(
        cls,
        msg: str,
        conn: AsyncConnection,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Logs a critical message to the database.

        Args:
            msg (str): The log message.
            conn (AsyncConnection): Asynchronous database connection.
            extra (Dict[str, Any]): Extra parameters. Defaults to 
                {"application_name": "default_name"}.
        """
        level: str = "CRITICAL"

        await cls.__log(
            cls,
            msg=msg,
            conn=conn,
            level=level,
            extra=extra,
        )
