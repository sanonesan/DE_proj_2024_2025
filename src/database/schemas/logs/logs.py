# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.27.0
# source: logs.sql
# pylint: disable-all
import dataclasses
import datetime
from typing import AsyncIterator, Optional

import sqlalchemy
import sqlalchemy.ext.asyncio

from src.database.schemas.logs import models


CREATE_LOG = """-- name: create_log \\:exec
INSERT INTO logs.application_logs (
    application_name,
    log_timestamp,
    log_level,
    log_message
) VALUES (
    :p1,
    :p2,
    :p3,
    :p4
)
"""


@dataclasses.dataclass()
class CreateLogParams:
    application_name: Optional[str]
    log_timestamp: Optional[datetime.datetime]
    log_level: Optional[str]
    log_message: Optional[str]


GET_LOGS = """-- name: get_logs \\:many
SELECT 
    log_id, application_name, log_timestamp, log_level, log_message
FROM 
    logs.application_logs
"""


class AsyncQuerier:
    def __init__(self, conn: sqlalchemy.ext.asyncio.AsyncConnection):
        self._conn = conn

    async def create_log(self, arg: CreateLogParams) -> None:
        await self._conn.execute(sqlalchemy.text(CREATE_LOG), {
            "p1": arg.application_name,
            "p2": arg.log_timestamp,
            "p3": arg.log_level,
            "p4": arg.log_message,
        })

    async def get_logs(self) -> AsyncIterator[models.LogsApplicationLog]:
        result = await self._conn.stream(sqlalchemy.text(GET_LOGS))
        async for row in result:
            yield models.LogsApplicationLog(
                log_id=row[0],
                application_name=row[1],
                log_timestamp=row[2],
                log_level=row[3],
                log_message=row[4],
            )
