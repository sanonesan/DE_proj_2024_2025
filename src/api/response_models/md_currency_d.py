"""
Response models for ds.md_currency_d routers
"""

from typing import List
from dataclasses import dataclass

from pydantic import BaseModel

from src.database.schemas.ds.models import DsMdCurrencyD

# ---------------------------
# GET \ PUT Response Classes
# ---------------------------


@dataclass
class MDCurrencyModel(DsMdCurrencyD):
    """
    md_currency_d response model
    for single returned value
    """


class AllMDCurrencyModel(BaseModel):
    """
    md_currency_d response model
    for multiple returned values
    """

    posts: List[MDCurrencyModel]


# ---------------------------
# POST Response Classes
# ---------------------------


class PostMDCurrencyModel(BaseModel):
    """
    md_currency_d response model
    for single posted value
    """

    resonse: str


class PostMultipleMDCurrencyModel(PostMDCurrencyModel):
    """
    md_currency_d response model
    for multiple posted values
    """

    count: int  # number of items posted
