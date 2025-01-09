# pylint: disable=R0801
"""
Router for ETL in ds.md_ledger_account_s
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
from src.api.response_models.md_ledger_account_s import (
    MDLedgerAccountModel,
    AllMDLedgerAccountModel,
    # PostMDLedgerAccountModel,
    PostMultipleMDLedgerAccountModel,
)

from src.database.schemas.ds.md_ledger_account_s import (
    AsyncQuerier,
    CreateMDLedgerAccountParams,
)

from src.logs.console_logger import LOGGER
from src.logs.database_logger import AsyncDatabaseLogger


ledger_account_router = APIRouter(
    tags=["DsMdLedgerAccountS"], prefix="/md_ledger_account_s"
)


@ledger_account_router.get(
    path="/",
    response_model=AllMDLedgerAccountModel,
)
async def get_all(
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> AllMDLedgerAccountModel:
    """
    Retrieves all ledger accounts records from the database.

    Args:
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A AllMDLedgerAccountModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start extracting * from md_ledger_account_s",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)
        accounts = querier.get_md_ledger_account()

        result = []
        async for account in accounts:
            result.append(
                MDLedgerAccountModel(
                    chapter=account.chapter,
                    chapter_name=account.chapter_name,
                    section_number=account.section_number,
                    section_name=account.section_name,
                    subsection_name=account.subsection_name,
                    ledger1_account=account.ledger1_account,
                    ledger1_account_name=account.ledger1_account_name,
                    ledger_account=account.ledger_account,
                    ledger_account_name=account.ledger_account_name,
                    characteristic=account.characteristic,
                    is_resident=account.is_resident,
                    is_reserve=account.is_reserve,
                    is_reserved=account.is_reserved,
                    is_loan=account.is_loan,
                    is_reserved_assets=account.is_reserved_assets,
                    is_overdue=account.is_overdue,
                    is_interest=account.is_interest,
                    pair_account=account.pair_account,
                    start_date=account.start_date,
                    end_date=account.end_date,
                    is_rub_only=account.is_rub_only,
                    min_term=account.min_term,
                    min_term_measure=account.min_term_measure,
                    max_term=account.max_term,
                    max_term_measure=account.max_term_measure,
                    ledger_acc_full_name_translit=account.ledger_acc_full_name_translit,
                    is_revaluation=account.is_revaluation,
                    is_correct=account.is_correct,
                )
            )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Data from md_ledger_account_s extracted!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return AllMDLedgerAccountModel(accounts=result)

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while extracting md_ledger_account_s: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while extracting md_ledger_account_s: {e}")


@ledger_account_router.post(
    path="/load_from_csv/",
    response_model=PostMultipleMDLedgerAccountModel,
    status_code=status.HTTP_201_CREATED,
)
async def load_from_csv(
    csv_path: str = SETTINGS.md_ledger_account_s_csv_path,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> PostMultipleMDLedgerAccountModel:
    """
    Loads posting data from a CSV file into the database.

    Args:
        csv_path: The path to the CSV file containing posting data (defaults to settings).
        conn: An async database connection to the primary database (dependency injected).
        logger_conn: An optional async database connection
            to the logger database (dependency injected).

    Returns:
        A PostMultipleMDLedgerAccountModel containing a confirmation response.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start loading md_ledger_account_s from csv",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        querier = AsyncQuerier(conn)

        counter = 0
        with open(csv_path, newline="", errors="replace", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                try:
                    account = CreateMDLedgerAccountParams(
                        chapter=str(row["CHAPTER"]),
                        chapter_name=str(row["CHAPTER_NAME"]),
                        section_number=int(row["SECTION_NUMBER"]),
                        section_name=str(row["SECTION_NAME"]),
                        subsection_name=str(row["SUBSECTION_NAME"]),
                        ledger1_account=int(row["LEDGER1_ACCOUNT"]),
                        ledger1_account_name=str(row["LEDGER1_ACCOUNT_NAME"]),
                        ledger_account=int(row["LEDGER_ACCOUNT"]),
                        ledger_account_name=str(row["LEDGER_ACCOUNT_NAME"]),
                        characteristic=str(row["CHARACTERISTIC"]),
                        start_date=datetime.datetime.strptime(
                            row["START_DATE"], "%Y-%m-%d"
                        ).date(),
                        end_date=datetime.datetime.strptime(
                            row["END_DATE"], "%Y-%m-%d"
                        ).date(),
                        #
                        # UNCOMMENT IF FIElDS APPEARE IN LOADED TABLE
                        #
                        # is_resident=int(row["IS_RESIDENT"]),
                        # is_reserve=int(row["IS_RESERVE"]),
                        # is_reserved=int(row["IS_RESERVED"]),
                        # is_loan=int(row["IS_LOAN"]),
                        # is_reserved_assets=int(row["IS_RESERVED_ASSETS"]),
                        # is_overdue=int(row["IS_OVERDUE"]),
                        # is_interest=int(row["IS_INTEREST"]),
                        # pair_account=str(row["PAIR_ACCOUNT"]),
                        # is_rub_only=int(row["IS_RUB_ONLY"]),
                        # min_term=str(row["MIN_TERM"]),
                        # min_term_measure=str(row["MIN_TERM_MEASURE"]),
                        # max_term=str(row["MAX_TERM"]),
                        # max_term_measure=str(row["MAX_TERM_MEASURE"]),
                        # ledger_acc_full_name_translit=str(row["LEDGER_ACC_FULL_NAME_TRANSLIT"]),
                        # is_revaluation=str(row["IS_REVALUATION"]),
                        # is_correct=str(row["IS_CORRECT"]),
                    )
                    await querier.create_md_ledger_account(account)
                    counter += 1
                except Exception as e:
                    if logger_conn:
                        await AsyncDatabaseLogger.error(
                            msg=f"Error while loading md_ledger_account_s: {e}"
                            f"\n\nCheck if fields `ledger_account`, `start_date`"
                            "are not empty {account}",
                            extra={"application_name": APPLICATION_NAME},
                            conn=logger_conn,
                        )
                    LOGGER.error(
                        msg=f"Error while loading md_ledger_account_s: {e}"
                        f"\n\nCheck if fields `ledger_account`, `start_date`"
                        "are not empty {account}",
                    )
                    continue

        await conn.commit()

        if logger_conn:
            await asyncio.sleep(2)
            await AsyncDatabaseLogger.info(
                msg="md_ledger_account_s loaded!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return PostMultipleMDLedgerAccountModel(
            resonse=f"md_ledger_account_s from {csv_path} posted!",
            count=counter,
        )

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while loading md_ledger_account_s: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while loading md_ledger_account_s: {e}")
