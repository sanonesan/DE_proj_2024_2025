"""
Response models for ds.md_exchange_rate_d routers
"""

from typing import List
from dataclasses import dataclass

from pydantic import BaseModel

from src.database.schemas.ds.models import DsMdExchangeRateD

# ---------------------------
# GET \ PUT Response Classes
# ---------------------------


@dataclass
class MDExchangeRateModel(DsMdExchangeRateD):
    """
    md_exchange_rate_d response model
    for single returned value
    """


class AllMDExchangeRateModel(BaseModel):
    """
    md_exchange_rate_d response model
    for multiple returned values
    """

    exchange_rates: List[MDExchangeRateModel]


# ---------------------------
# POST Response Classes
# ---------------------------


class PostMDExchangeRateModel(BaseModel):
    """
    md_exchange_rate_d response model
    for single posted value
    """

    resonse: str


class PostMultipleMDExchangeRateModel(PostMDExchangeRateModel):
    """
    md_exchange_rate_d response model
    for multiple posted values
    """

    count: int  # number of items posted
