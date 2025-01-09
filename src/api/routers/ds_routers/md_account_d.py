# pylint: disable=R0801
"""
Router for ETL in ds.md_account_d
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
from src.api.response_models.md_account_d import (
    MDAccountModel,
    AllMDAccountModel,
    # PostMDAccountModel,
    PostMultipleMDAccountModel,
)

from src.database.schemas.ds.md_account_d import AsyncQuerier, CreateMDAccountParams

from src.logs.console_logger import LOGGER
from src.logs.database_logger import AsyncDatabaseLogger


account_router = APIRouter(tags=["DsMdAccountD"], prefix="/md_account_d")


@account_router.get(
    path="/",
    response_model=AllMDAccountModel,
)
async def get_all(
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> AllMDAccountModel:
    """
    Retrieves all accounts records from the database.

    Args:
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A AllMDAccountModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start extracting * from md_account_d",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)
        accounts = querier.get_md_accounts()

        result = []
        async for account in accounts:
            result.append(
                MDAccountModel(
                    data_actual_date=account.data_actual_date,
                    data_actual_end_date=account.data_actual_end_date,
                    account_rk=account.account_rk,
                    account_number=account.account_number,
                    char_type=account.char_type,
                    currency_rk=account.currency_rk,
                    currency_code=account.currency_code,
                )
            )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Data from md_account_d extracted!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return AllMDAccountModel(posts=result)

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while extracting md_account_d: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while extracting md_account_d: {e}")


@account_router.post(
    path="/load_from_csv/",
    response_model=PostMultipleMDAccountModel,
    status_code=status.HTTP_201_CREATED,
)
async def load_from_csv(
    csv_path: str = SETTINGS.md_account_d_csv_path,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> PostMultipleMDAccountModel:
    """
    Loads posting data from a CSV file into the database.

    Args:
        csv_path: The path to the CSV file containing posting data (defaults to settings).
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A PostMultipleMDAccountModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start loading md_account_d from csv",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)

        counter = 0
        with open(csv_path, newline="", errors="replace", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                await querier.create_md_account(
                    CreateMDAccountParams(
                        data_actual_date=datetime.datetime.strptime(
                            row["DATA_ACTUAL_DATE"], "%Y-%m-%d"
                        ).date(),
                        data_actual_end_date=datetime.datetime.strptime(
                            row["DATA_ACTUAL_END_DATE"], "%Y-%m-%d"
                        ).date(),
                        account_rk=int(row["ACCOUNT_RK"]),
                        account_number=str(row["ACCOUNT_NUMBER"]),
                        char_type=str(row["CHAR_TYPE"]),
                        currency_rk=int(row["CURRENCY_RK"]),
                        currency_code=str(row["CURRENCY_CODE"]),
                    )
                )
                counter += 1

        await conn.commit()

        if logger_conn:
            await asyncio.sleep(2)
            await AsyncDatabaseLogger.info(
                msg="md_account_d loaded!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return PostMultipleMDAccountModel(
            resonse=f"Accounts from {csv_path} posted!",
            count=counter,
        )

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while loading md_account_d: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while loading md_account_d: {e}")
