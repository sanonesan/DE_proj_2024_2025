# pylint: disable=R0801
"""
Router for ETL in ds.ft_posting_f
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
from src.api.response_models.ft_posting_f import (
    PostingModel,
    AllPostingModel,
    # PostPostingModel,
    PostMultiplePostingModel,
    DeletePostingModel,
)

from src.database.schemas.ds.ft_posting_f import AsyncQuerier, CreatePostParams

from src.logs.console_logger import LOGGER
from src.logs.database_logger import AsyncDatabaseLogger


posting_router = APIRouter(tags=["DsFtPostingF"], prefix="/ft_posting_f")


@posting_router.get(
    path="/",
    response_model=AllPostingModel,
)
async def get_all(
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> AllPostingModel:
    """
    Retrieves all posting records from the database.

    Args:
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection 
            to the logger database (dependency injected).

    Returns:
        A AllPostingModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start extracting * from ft_posting_f",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)
        posts = querier.get_posts()

        result = []
        async for post in posts:
            result.append(
                PostingModel(
                    oper_date=post.oper_date,
                    credit_account_rk=post.credit_account_rk,
                    debet_account_rk=post.debet_account_rk,
                    credit_amount=post.credit_amount,
                    debet_amount=post.debet_amount,
                )
            )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Data from ft_posting_f extracted!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return AllPostingModel(posts=result)

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while extracting ft_posting_f: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while extracting ft_posting_f: {e}")


@posting_router.delete(path="/truncate_table/", response_model=DeletePostingModel)
async def truncate_table(
    confirm: bool = False,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> DeletePostingModel:
    """
    Deletes all posting records from the database.

    Args:
        confirm: confirmation for deletation.
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection 
            to the logger database (dependency injected).

    Returns:
        A DeletePostingModel containing a confirmation response.
    """

    try:
        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start truncating ft_posting_f",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        if confirm:

            querier = AsyncQuerier(conn)

            await querier.truncate_posting_table()

            await conn.commit()

            if logger_conn:
                await AsyncDatabaseLogger.info(
                    msg="ft_posting_f truncated!",
                    extra={"application_name": APPLICATION_NAME},
                    conn=logger_conn,
                )

            return DeletePostingModel(
                content="Table ft_posting_f truncated!",
                operation_result=True,
                status_code=status.HTTP_204_NO_CONTENT,
            )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Truncating stopped: NO CONFIRMATION",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return DeletePostingModel(
            content="Truncating stopped: NO CONFIRMATION!",
            operation_result=False,
            status_code=status.HTTP_403_FORBIDDEN,
        )

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while truncating ft_posting_f: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while truncating ft_posting_f: {e}")

        return DeletePostingModel(
            content="Truncating stopped: Error!",
            operation_result=False,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@posting_router.post(
    path="/load_from_csv/",
    response_model=PostMultiplePostingModel,
    status_code=status.HTTP_201_CREATED,
)
async def load_from_csv(
    csv_path: str = SETTINGS.ft_posting_f_csv_path,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> PostMultiplePostingModel:
    """
    Loads posting data from a CSV file into the database.

    Args:
        csv_path: The path to the CSV file containing posting data (defaults to settings).
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection 
            to the logger database (dependency injected).

    Returns:
        A PostMultiplePostingModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start loading ft_posting_f from csv",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        # ------CONDITION FOR TRUNCATING TABLE --------
        # ВАЖНО: У DS_FT_POSTING_F нет первичного ключа.
        # Перед каждой загрузкой таблицу нужно очищать!
        truncation = await truncate_table(
            confirm=True,
            conn=conn,
            logger_conn=logger_conn,
        )

        if truncation.operation_result:

            querier = AsyncQuerier(conn)

            counter = 0
            with open(
                csv_path, newline="", errors="replace", encoding="utf-8"
            ) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")

                for row in reader:

                    await querier.create_post(
                        CreatePostParams(
                            oper_date=datetime.datetime.strptime(
                                row["OPER_DATE"], "%d-%m-%Y"
                            ).date(),
                            credit_account_rk=int(row["CREDIT_ACCOUNT_RK"]),
                            debet_account_rk=int(row["DEBET_ACCOUNT_RK"]),
                            credit_amount=float(row["CREDIT_AMOUNT"]),
                            debet_amount=float(row["DEBET_AMOUNT"]),
                        )
                    )
                    counter += 1

            await conn.commit()

            if logger_conn:
                await asyncio.sleep(2)
                await AsyncDatabaseLogger.info(
                    msg="ft_posting_f loaded!",
                    extra={"application_name": APPLICATION_NAME},
                    conn=logger_conn,
                )

            return PostMultiplePostingModel(
                resonse=f"ft_posting_f from {csv_path} posted!",
                count=counter,
            )

        return PostMultiplePostingModel(
            resonse=f"Nothing posted to ft_posting_f from {csv_path}:"
            "UNABLE TO TRUNCATE TABLE!",
            count=0,
        )

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while loading ft_posting_f: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while loading ft_posting_f: {e}")
