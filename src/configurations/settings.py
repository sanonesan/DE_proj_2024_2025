"""
Default settings for database connections and paths to data
"""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Class with default settings for application
    """
    ds_database_url: str
    logger_database_url: str
    echo_sql: bool = False
    test: bool = False
    project_name: str = "ETL proj"
    ft_balance_f_csv_path: str = "./data/load/ft_balance_f.csv"
    ft_posting_f_csv_path: str = "./data/load/ft_posting_f.csv"
    md_account_d_csv_path: str = "./data/load/md_account_d.csv"
    md_exchange_rate_d_csv_path: str = "./data/load/md_exchange_rate_d.csv"
    md_currency_d_csv_path: str = "./data/load/md_currency_d.csv"
    md_ledger_account_s_csv_path: str = "./data/load/md_ledger_account_s.csv"


load_dotenv()
SETTINGS = Settings(
    ds_database_url=os.getenv("DATABASE_DS_URL"),
    logger_database_url=os.getenv("DATABASE_LOGGER_URL"),
)
