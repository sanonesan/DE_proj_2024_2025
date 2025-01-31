# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.27.0
# pylint: disable-all
import dataclasses
import datetime
from typing import Optional


@dataclasses.dataclass()
class DsFtBalanceF:
    on_date: datetime.date
    account_rk: int
    currency_rk: int
    balance_out: Optional[float]


@dataclasses.dataclass()
class DsFtPostingF:
    oper_date: datetime.date
    credit_account_rk: int
    debet_account_rk: int
    credit_amount: Optional[float]
    debet_amount: Optional[float]


@dataclasses.dataclass()
class DsMdAccountD:
    data_actual_date: datetime.date
    data_actual_end_date: datetime.date
    account_rk: int
    account_number: str
    char_type: str
    currency_rk: int
    currency_code: str


@dataclasses.dataclass()
class DsMdCurrencyD:
    currency_rk: int
    data_actual_date: datetime.date
    data_actual_end_date: Optional[datetime.date]
    currency_code: Optional[str]
    code_iso_char: Optional[str]


@dataclasses.dataclass()
class DsMdExchangeRateD:
    data_actual_date: datetime.date
    data_actual_end_date: Optional[datetime.date]
    currency_rk: int
    reduced_cource: Optional[float]
    code_iso_num: Optional[str]


@dataclasses.dataclass()
class DsMdLedgerAccount:
    chapter: Optional[str]
    chapter_name: Optional[str]
    section_number: Optional[int]
    section_name: Optional[str]
    subsection_name: Optional[str]
    ledger1_account: Optional[int]
    ledger1_account_name: Optional[str]
    ledger_account: int
    ledger_account_name: Optional[str]
    characteristic: Optional[str]
    is_resident: Optional[int]
    is_reserve: Optional[int]
    is_reserved: Optional[int]
    is_loan: Optional[int]
    is_reserved_assets: Optional[int]
    is_overdue: Optional[int]
    is_interest: Optional[int]
    pair_account: Optional[str]
    start_date: datetime.date
    end_date: Optional[datetime.date]
    is_rub_only: Optional[int]
    min_term: Optional[str]
    min_term_measure: Optional[str]
    max_term: Optional[str]
    max_term_measure: Optional[str]
    ledger_acc_full_name_translit: Optional[str]
    is_revaluation: Optional[str]
    is_correct: Optional[str]
