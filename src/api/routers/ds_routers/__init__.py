"""
Assemble DS routers
"""

from fastapi import APIRouter

from src.api.routers.ds_routers.ft_balance_f import balance_router
from src.api.routers.ds_routers.ft_posting_f import posting_router
from src.api.routers.ds_routers.md_account_d import account_router
from src.api.routers.ds_routers.md_currency_d import currency_router
from src.api.routers.ds_routers.md_exchange_rate_d import exchange_rate_router
from src.api.routers.ds_routers.md_ledger_account_s import ledger_account_router

from src.api.routers.ds_routers.ds_etl_process import ds_etl_router

# Import router
ds_router = APIRouter(prefix="/ds")

# Include routers
ds_router.include_router(balance_router)
ds_router.include_router(posting_router)
ds_router.include_router(account_router)
ds_router.include_router(currency_router)
ds_router.include_router(exchange_rate_router)
ds_router.include_router(ledger_account_router)

ds_router.include_router(ds_etl_router)
