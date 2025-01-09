-- ВАЖНО: У DS_FT_POSTING_F нет первичного ключа.
-- Перед каждой загрузкой таблицу нужно очищать!
CREATE TABLE
    ds.FT_POSTING_F (
        oper_date DATE NOT NULL,
        credit_account_rk INTEGER NOT NULL,
        debet_account_rk INTEGER NOT NULL,
        credit_amount FLOAT,
        debet_amount FLOAT
    );