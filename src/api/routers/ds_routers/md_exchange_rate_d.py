# pylint: disable=R0801
"""
Router for ETL in ds.md_exchange_rate_d
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
from src.api.response_models.md_exchange_rate_d import (
    MDExchangeRateModel,
    AllMDExchangeRateModel,
    # PostMDExchangeRateModel,
    PostMultipleMDExchangeRateModel,
)

from src.database.schemas.ds.md_exchange_rate_d import (
    AsyncQuerier,
    CreateMDExchangeRateParams,
)

from src.logs.console_logger import LOGGER
from src.logs.database_logger import AsyncDatabaseLogger


exchange_rate_router = APIRouter(
    tags=["DsMdExchangeRateD"], prefix="/md_exchange_rate_d"
)


@exchange_rate_router.get(
    path="/",
    response_model=AllMDExchangeRateModel,
)
async def get_all(
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> AllMDExchangeRateModel:
    """
    Retrieves all exchange rate records from the database.

    Args:
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A AllMDExchangeRateModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start extracting * from md_exchange_rate_d",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)
        rates = querier.get_md_exchange_rate()

        result = []
        async for rate in rates:
            result.append(
                MDExchangeRateModel(
                    data_actual_date=rate.data_actual_date,
                    data_actual_end_date=rate.data_actual_end_date,
                    currency_rk=rate.currency_rk,
                    reduced_cource=rate.reduced_cource,
                    code_iso_num=rate.code_iso_num,
                )
            )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Data from md_exchange_rate_d extracted!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return AllMDExchangeRateModel(exchange_rates=result)

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while extracting md_exchange_rate_d: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while extracting md_exchange_rate_d: {e}")


@exchange_rate_router.post(
    path="/load_from_csv/",
    response_model=PostMultipleMDExchangeRateModel,
    status_code=status.HTTP_201_CREATED,
)
async def load_from_csv(
    csv_path: str = SETTINGS.md_exchange_rate_d_csv_path,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> PostMultipleMDExchangeRateModel:
    """
    Loads posting data from a CSV file into the database.

    Args:
        csv_path: The path to the CSV file containing posting data (defaults to settings).
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A PostMultipleMDExchangeRateModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start loading md_exchange_rate_d from csv",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)

        counter = 0
        with open(csv_path, newline="", errors="replace", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                await querier.create_md_exchange_rate(
                    CreateMDExchangeRateParams(
                        data_actual_date=datetime.datetime.strptime(
                            row["DATA_ACTUAL_DATE"], "%Y-%m-%d"
                        ).date(),
                        data_actual_end_date=datetime.datetime.strptime(
                            row["DATA_ACTUAL_END_DATE"], "%Y-%m-%d"
                        ).date(),
                        currency_rk=int(row["CURRENCY_RK"]),
                        reduced_cource=float(row["REDUCED_COURCE"]),
                        code_iso_num=str(row["CODE_ISO_NUM"]),
                    )
                )
                counter += 1

        await conn.commit()

        if logger_conn:
            await asyncio.sleep(2)
            await AsyncDatabaseLogger.info(
                msg="md_exchange_rate_d loaded!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return PostMultipleMDExchangeRateModel(
            resonse=f"md_exchange_rate_d from {csv_path} posted!",
            count=counter,
        )

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while loading md_exchange_rate_d: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while loading md_exchange_rate_d: {e}")
        LOGGER.error(msg=f"Error while loading md_exchange_rate_d: {counter}")
