# pylint: disable=R0801
"""
Router for ETL in ds.ft_balance_f
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
from src.api.response_models.ft_balance_f import (
    BalanceModel,
    AllBalancesModel,
    # PostBalanceModel,
    PostMultipleBalancesModel,
)

from src.database.schemas.ds.ft_balance_f import AsyncQuerier, CreateBalanceParams

from src.logs.console_logger import LOGGER
from src.logs.database_logger import AsyncDatabaseLogger


balance_router = APIRouter(tags=["DsFtBalanceF"], prefix="/ft_balance_f")


@balance_router.get(
    path="/",
    response_model=AllBalancesModel,
)
async def get_all(
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> AllBalancesModel:
    """
    Retrieves all balance records from the database.

    Args:
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection 
            to the logger database (dependency injected).

    Returns:
        A AllBalancesModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start extracting * from ft_balance_f",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)
        balances = querier.get_balance()

        result = []
        async for balance in balances:
            result.append(
                BalanceModel(
                    on_date=balance.on_date,
                    account_rk=balance.account_rk,
                    currency_rk=balance.currency_rk,
                    balance_out=balance.balance_out,
                )
            )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Data from ft_balance_f extracted!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return AllBalancesModel(balances=result)

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while extracting ft_balance_f: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while extracting ft_balance_f: {e}")


@balance_router.post(
    path="/load_from_csv/",
    response_model=PostMultipleBalancesModel,
    status_code=status.HTTP_201_CREATED,
)
async def load_from_csv(
    csv_path: str = SETTINGS.ft_balance_f_csv_path,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> PostMultipleBalancesModel:
    """
    Loads posting data from a CSV file into the database.

    Args:
        csv_path: The path to the CSV file containing posting data (defaults to settings).
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection 
            to the logger database (dependency injected).

    Returns:
        A PostMultipleBalancesModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start loading ft_balance_f from csv",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)

        counter = 0
        with open(csv_path, newline="", errors="replace", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                await querier.create_balance(
                    CreateBalanceParams(
                        on_date=datetime.datetime.strptime(
                            row["ON_DATE"], "%d.%m.%Y"
                        ).date(),
                        account_rk=int(row["ACCOUNT_RK"]),
                        currency_rk=int(row["CURRENCY_RK"]),
                        balance_out=float(row["BALANCE_OUT"]),
                    )
                )
                counter += 1
        await conn.commit()

        if logger_conn:
            await asyncio.sleep(2)
            await AsyncDatabaseLogger.info(
                msg="ft_balance_f loaded!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return PostMultipleBalancesModel(
            resonse=f"ft_balance_f from {csv_path} posted!",
            count=counter,
        )

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while loading ft_balance_f: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while loading ft_balance_f: {e}")
