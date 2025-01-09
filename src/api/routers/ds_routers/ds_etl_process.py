"""
Router for full ETL process for DS schema
"""

from typing import Optional

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncConnection

from src.configurations.database import (
    async_ds_db_connection,
    async_logger_db_connection,
)

from src.api.response_models.ft_balance_f import (
    PostMultipleBalancesModel,
)


from src.configurations.settings import SETTINGS

from src.api import APPLICATION_NAME
from src.logs.console_logger import LOGGER
from src.logs.database_logger import AsyncDatabaseLogger


from src.api.routers.ds_routers.ft_balance_f import (
    load_from_csv as ft_balance_f_load_from_csv,
)
from src.api.routers.ds_routers.ft_posting_f import (
    load_from_csv as ft_posting_f_load_from_csv,
)
from src.api.routers.ds_routers.md_account_d import (
    load_from_csv as md_account_d_load_from_csv,
)
from src.api.routers.ds_routers.md_currency_d import (
    load_from_csv as md_currency_d_load_from_csv,
)
from src.api.routers.ds_routers.md_exchange_rate_d import (
    load_from_csv as md_exchange_rate_d_load_from_csv,
)
from src.api.routers.ds_routers.md_ledger_account_s import (
    load_from_csv as md_ledger_account_s_load_from_csv,
)

ds_etl_router = APIRouter(tags=["DsFullEtl"], prefix="/general")

@ds_etl_router.post(
    path="/load_all_tables_from_csv/",
    response_model=PostMultipleBalancesModel,
    status_code=status.HTTP_201_CREATED,
)
async def load_from_csv( # pylint: disable=too-many-arguments, too-many-positional-arguments
    ft_balance_f_csv_path: str = SETTINGS.ft_balance_f_csv_path,
    ft_posting_f_csv_path: str = SETTINGS.ft_posting_f_csv_path,
    md_account_d_csv_path: str = SETTINGS.md_account_d_csv_path,
    md_currency_d_csv_path: str = SETTINGS.md_currency_d_csv_path,
    md_exchange_rate_d_csv_path: str = SETTINGS.md_exchange_rate_d_csv_path,
    md_ledger_account_s_csv_path: str = SETTINGS.md_ledger_account_s_csv_path,
    conn: AsyncConnection = Depends(async_ds_db_connection),
    logger_conn: Optional[AsyncConnection] = Depends(async_logger_db_connection),
) -> Response:
    """
    Loads and updates data from CSV files into corresponding database tables.

    This function reads data from specified CSV files (for fact and dimension tables)
    and inserts or updates the data into the designated tables.

    Args:
        ft_balance_f_csv_path: Path to the CSV file for the FT_BALANCE_F table.
        ft_posting_f_csv_path: Path to the CSV file for the FT_POSTING_F table.
        md_account_d_csv_path: Path to the CSV file for the MD_ACCOUNT_D table.
        md_currency_d_csv_path: Path to the CSV file for the MD_CURRENCY_D table.
        md_exchange_rate_d_csv_path: Path to the CSV file for the MD_EXCHANGE_RATE_D table.
        md_ledger_account_s_csv_path: Path to the CSV file for the MD_LEDGER_ACCOUNT_S table.
        conn: Asynchronous database connection for the main data source (dependency-injected).
        logger_conn: Optional asynchronous database connection for logging (dependency-injected).

    Returns:
        A FastAPI Response object indicating the outcome of the operation.
    """

    try:

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="Start loading DS TABLES from csv",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        await ft_balance_f_load_from_csv(
            ft_balance_f_csv_path,
            conn=conn,
            logger_conn=logger_conn,
        )

        await ft_posting_f_load_from_csv(
            ft_posting_f_csv_path,
            conn=conn,
            logger_conn=logger_conn,
        )

        await md_account_d_load_from_csv(
            md_account_d_csv_path,
            conn=conn,
            logger_conn=logger_conn,
        )

        await md_currency_d_load_from_csv(
            md_currency_d_csv_path,
            conn=conn,
            logger_conn=logger_conn,
        )

        await md_exchange_rate_d_load_from_csv(
            md_exchange_rate_d_csv_path,
            conn=conn,
            logger_conn=logger_conn,
        )

        await md_ledger_account_s_load_from_csv(
            md_ledger_account_s_csv_path,
            conn=conn,
            logger_conn=logger_conn,
        )

        if logger_conn:
            await AsyncDatabaseLogger.info(
                msg="DS TABLES loaded!",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )

        return Response(content="DS ETL DONE!", status_code=status.HTTP_200_OK)

    except Exception as e:
        if logger_conn:
            await AsyncDatabaseLogger.error(
                msg=f"Error while loading DS TABLES: {e}",
                extra={"application_name": APPLICATION_NAME},
                conn=logger_conn,
            )
        LOGGER.error(msg=f"Error while loading DS TABLES: {e}")
