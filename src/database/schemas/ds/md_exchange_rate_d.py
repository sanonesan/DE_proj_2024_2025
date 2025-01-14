# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.27.0
# source: md_exchange_rate_d.sql
# pylint: disable-all
import dataclasses
import datetime
from typing import AsyncIterator, Optional

import sqlalchemy
import sqlalchemy.ext.asyncio

from src.database.schemas.ds import models


CREATE_MD_EXCHANGE_RATE = """-- name: create_md_exchange_rate \\:exec
INSERT INTO ds.MD_EXCHANGE_RATE_D (
    data_actual_date,
    data_actual_end_date,
    currency_rk,
    reduced_cource,
    code_iso_num
) VALUES (
    :p1,
    :p2,
    :p3,
    :p4,
    :p5
)
ON CONFLICT (data_actual_date, currency_rk) 
DO UPDATE SET
    data_actual_end_date=EXCLUDED.data_actual_end_date,
    reduced_cource=EXCLUDED.reduced_cource,
    code_iso_num=EXCLUDED.code_iso_num
WHERE NOT (
    ds.MD_EXCHANGE_RATE_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_EXCHANGE_RATE_D.reduced_cource=EXCLUDED.reduced_cource
    AND ds.MD_EXCHANGE_RATE_D.code_iso_num=EXCLUDED.code_iso_num
)
"""


@dataclasses.dataclass()
class CreateMDExchangeRateParams:
    data_actual_date: datetime.date
    data_actual_end_date: Optional[datetime.date]
    currency_rk: int
    reduced_cource: Optional[float]
    code_iso_num: Optional[str]


CREATE_MD_EXCHANGE_RATE_RETURN = """-- name: create_md_exchange_rate_return \\:one
INSERT INTO ds.MD_EXCHANGE_RATE_D (
    data_actual_date,
    data_actual_end_date,
    currency_rk,
    reduced_cource,
    code_iso_num
) VALUES (
    :p1,
    :p2,
    :p3,
    :p4,
    :p5
)
ON CONFLICT (data_actual_date, currency_rk) 
DO UPDATE SET
    data_actual_end_date=EXCLUDED.data_actual_end_date,
    reduced_cource=EXCLUDED.reduced_cource,
    code_iso_num=EXCLUDED.code_iso_num
WHERE NOT (
    ds.MD_EXCHANGE_RATE_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_EXCHANGE_RATE_D.reduced_cource=EXCLUDED.reduced_cource
    AND ds.MD_EXCHANGE_RATE_D.code_iso_num=EXCLUDED.code_iso_num
)
RETURNING data_actual_date, data_actual_end_date, currency_rk, reduced_cource, code_iso_num
"""


@dataclasses.dataclass()
class CreateMDExchangeRateReturnParams:
    data_actual_date: datetime.date
    data_actual_end_date: Optional[datetime.date]
    currency_rk: int
    reduced_cource: Optional[float]
    code_iso_num: Optional[str]


GET_MD_EXCHANGE_RATE = """-- name: get_md_exchange_rate \\:many
SELECT
    data_actual_date, data_actual_end_date, currency_rk, reduced_cource, code_iso_num
FROM
    ds.MD_EXCHANGE_RATE_D
"""


class AsyncQuerier:
    def __init__(self, conn: sqlalchemy.ext.asyncio.AsyncConnection):
        self._conn = conn

    async def create_md_exchange_rate(self, arg: CreateMDExchangeRateParams) -> None:
        await self._conn.execute(sqlalchemy.text(CREATE_MD_EXCHANGE_RATE), {
            "p1": arg.data_actual_date,
            "p2": arg.data_actual_end_date,
            "p3": arg.currency_rk,
            "p4": arg.reduced_cource,
            "p5": arg.code_iso_num,
        })

    async def create_md_exchange_rate_return(self, arg: CreateMDExchangeRateReturnParams) -> Optional[models.DsMdExchangeRateD]:
        row = (await self._conn.execute(sqlalchemy.text(CREATE_MD_EXCHANGE_RATE_RETURN), {
            "p1": arg.data_actual_date,
            "p2": arg.data_actual_end_date,
            "p3": arg.currency_rk,
            "p4": arg.reduced_cource,
            "p5": arg.code_iso_num,
        })).first()
        if row is None:
            return None
        return models.DsMdExchangeRateD(
            data_actual_date=row[0],
            data_actual_end_date=row[1],
            currency_rk=row[2],
            reduced_cource=row[3],
            code_iso_num=row[4],
        )

    async def get_md_exchange_rate(self) -> AsyncIterator[models.DsMdExchangeRateD]:
        result = await self._conn.stream(sqlalchemy.text(GET_MD_EXCHANGE_RATE))
        async for row in result:
            yield models.DsMdExchangeRateD(
                data_actual_date=row[0],
                data_actual_end_date=row[1],
                currency_rk=row[2],
                reduced_cource=row[3],
                code_iso_num=row[4],
            )
