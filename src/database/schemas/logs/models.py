# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.27.0
# pylint: disable-all
import dataclasses
import datetime
from typing import Optional


@dataclasses.dataclass()
class LogsApplicationLog:
    log_id: int
    application_name: Optional[str]
    log_timestamp: Optional[datetime.datetime]
    log_level: Optional[str]
    log_message: Optional[str]