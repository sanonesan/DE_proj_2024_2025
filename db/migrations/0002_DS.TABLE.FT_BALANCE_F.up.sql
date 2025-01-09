-- Создание таблиц в схеме "ds"
CREATE TABLE
    ds.FT_BALANCE_F (
        on_date DATE NOT NULL,
        account_rk INTEGER NOT NULL,
        currency_rk INTEGER NOT NULL,
        balance_out FLOAT,
        PRIMARY KEY (on_date, account_rk)
    );