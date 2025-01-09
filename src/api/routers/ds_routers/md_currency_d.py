# pylint: disable=R0801
"""
Router for ETL in ds.md_currency_d
"""

import asyncio
import csv
import datetime
from typing import Optional

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncConnection


from src.configurations.database import (
    async_ds_db_connection,
    async_logger_db_connection,
)
from src.configurations.settings import SETTINGS

from src.api import APPLICATION_NAME
from src.api.response_models.md_currency_d import (
    MDCurrencyModel,
    AllMDCurrencyModel,
    # PostMDCurrencyModel,
    PostMultipleMDCurrencyModel,
)

from src.database.schemas.ds.md_currency_d import AsyncQuerier, CreateMDCurrencyParams

from src.logs.console_logger import LOGGER
from src.logs.database_logger import AsyncDatabaseLogger

currency_router = APIRouter(tags=["DsMdCurrencyD"], prefix="/md_currency_d")


@currency_router.get(
    path="/",
    response_model=AllMDCurrencyModel,
)
async def get_all(
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> AllMDCurrencyModel:
    """
    Retrieves all currency records from the database.

    Args:
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A AllMDCurrencyModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start extracting * from md_exchange_rate_d",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)
        currencies = querier.get_md_currency()

        result = []
        async for currency in currencies:
            result.append(
                MDCurrencyModel(
                    currency_rk=currency.currency_rk,
                    data_actual_date=currency.data_actual_date,
                    data_actual_end_date=currency.data_actual_end_date,
                    currency_code=currency.currency_code,
                    code_iso_char=currency.code_iso_char,
                )
            )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Data from md_currency_d extracted!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return AllMDCurrencyModel(posts=result)

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while extracting md_currency_d: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while extracting md_currency_d: {e}")


@currency_router.post(
    path="/load_from_csv/",
    response_model=PostMultipleMDCurrencyModel,
    status_code=status.HTTP_201_CREATED,
)
async def load_from_csv(
    csv_path: str = SETTINGS.md_currency_d_csv_path,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> PostMultipleMDCurrencyModel:
    """
    Loads posting data from a CSV file into the database.

    Args:
        csv_path: The path to the CSV file containing posting data (defaults to settings).
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A PostMultipleMDCurrencyModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start loading md_currency_d from csv",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)

        counter = 0
        with open(csv_path, newline="", errors="replace", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                await querier.create_md_currency(
                    CreateMDCurrencyParams(
                        currency_rk=int(row["CURRENCY_RK"]),
                        data_actual_date=datetime.datetime.strptime(
                            row["DATA_ACTUAL_DATE"], "%Y-%m-%d"
                        ).date(),
                        data_actual_end_date=datetime.datetime.strptime(
                            row["DATA_ACTUAL_END_DATE"], "%Y-%m-%d"
                        ).date(),
                        currency_code=str(row["CURRENCY_CODE"]),
                        code_iso_char=str(row["CODE_ISO_CHAR"]),
                    )
                )
                counter += 1

        await conn.commit()

        if logger_conn:
            await asyncio.sleep(2)
            await AsyncDatabaseLogger.info(
                msg="md_currency_d loaded!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return PostMultipleMDCurrencyModel(
            resonse=f"Currency from {csv_path} posted!",
            count=counter,
        )

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while loading md_currency_d: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while loading md_currency_d: {e}")
