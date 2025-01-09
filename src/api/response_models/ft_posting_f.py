"""
Response models for ds.ft_posting_f routers
"""

from typing import List, Optional
from dataclasses import dataclass

from pydantic import BaseModel

from src.database.schemas.ds.models import DsFtPostingF

# ---------------------------
# GET \ PUT Response Classes
# ---------------------------


@dataclass
class PostingModel(DsFtPostingF):
    """
    ft_posting_f response model
    for single returned value
    """


class AllPostingModel(BaseModel):
    """
    ft_balance_f response model
    for multiple returned values
    """

    posts: List[PostingModel]


# ---------------------------
# POST Response Classes
# ---------------------------


class PostPostingModel(BaseModel):
    """
    ft_balance_f response model
    for single posted value
    """

    resonse: str


class PostMultiplePostingModel(PostPostingModel):
    """
    ft_balance_f response model
    for multiple posted values
    """

    count: int  # number of items posted


# ---------------------------
# Delete Response Classes
# ---------------------------


class DeletePostingModel(BaseModel):
    """
    ft_balance_f response model
    for deletation from DS.FT_POSTING_F
    """

    content: Optional[str] = (None,)
    operation_result: bool = False
    status_code: int = (200,)
