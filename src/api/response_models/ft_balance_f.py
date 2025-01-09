"""
Response models for ds.ft_balance_f routers
"""

from typing import List
from dataclasses import dataclass

from pydantic import BaseModel

from src.database.schemas.ds.models import DsFtBalanceF

# ---------------------------
# GET \ PUT Response Classes
# ---------------------------

@dataclass
class BalanceModel(DsFtBalanceF):
    """
    ft_balance_f response model
    for single returned value
    """

class AllBalancesModel(BaseModel):
    """
    ft_balance_f response model
    for multiple returned values
    """
    balances: List[BalanceModel]


# ---------------------------
# POST Response Classes
# ---------------------------
class PostBalanceModel(BaseModel):
    """
    ft_balance_f response model
    for single posted value
    """
    resonse: str

class PostMultipleBalancesModel(PostBalanceModel):
    """
    ft_balance_f response model
    for multiple posted values
    """
    resonse: str
    count: int # number of items posted
