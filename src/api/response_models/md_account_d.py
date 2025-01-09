"""
Response models for ds.md_account_d routers
"""

from typing import List
from dataclasses import dataclass

from pydantic import BaseModel

from src.database.schemas.ds.models import DsMdAccountD

# ---------------------------
# GET \ PUT Response Classes
# ---------------------------


@dataclass
class MDAccountModel(DsMdAccountD):
    """
    md_account_d response model
    for single returned value
    """


class AllMDAccountModel(BaseModel):
    """
    md_account_d response model
    for multiple returned values
    """

    posts: List[MDAccountModel]


# ---------------------------
# POST Response Classes
# ---------------------------


class PostMDAccountModel(BaseModel):
    """
    md_account_d response model
    for single posted value
    """

    resonse: str


class PostMultipleMDAccountModel(PostMDAccountModel):
    """
    md_account_d response model
    for multiple posted values
    """

    count: int  # number of items posted
