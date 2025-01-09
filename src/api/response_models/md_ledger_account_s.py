"""
Response models for ds.md_ledger_account_s routers
"""

from typing import List
from dataclasses import dataclass

from pydantic import BaseModel

from src.database.schemas.ds.models import DsMdLedgerAccount

# ---------------------------
# GET \ PUT Response Classes
# ---------------------------


@dataclass
class MDLedgerAccountModel(DsMdLedgerAccount):
    """
    md_ledger_account_s response model
    for single returned value
    """


class AllMDLedgerAccountModel(BaseModel):
    """
    md_ledger_account_s response model
    for multiple returned values
    """

    accounts: List[MDLedgerAccountModel]


# ---------------------------
# POST Response Classes
# ---------------------------


class PostMDLedgerAccountModel(BaseModel):
    """
    md_ledger_account_s response model
    for single posted value
    """

    resonse: str


class PostMultipleMDLedgerAccountModel(PostMDLedgerAccountModel):
    """
    md_ledger_account_s response model
    for multiple posted values
    """

    count: int  # number of items posted
