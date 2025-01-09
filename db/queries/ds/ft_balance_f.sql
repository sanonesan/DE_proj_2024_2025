-- name: GetBalance :many
SELECT
    *
FROM
    ds.FT_BALANCE_F;

-- name: GetAccountBalance :many
SELECT
    *
FROM
    ds.FT_BALANCE_F
WHERE ds.FT_BALANCE_F.account_rk = $1;


-- name: CreateBalance :exec
INSERT INTO
    ds.FT_BALANCE_F (on_date, account_rk, currency_rk, balance_out)
VALUES
    ($1, $2, $3, $4)
ON CONFLICT (on_date, account_rk) 
DO UPDATE SET
    currency_rk=EXCLUDED.currency_rk,
    balance_out=EXCLUDED.balance_out
WHERE NOT (
    ds.FT_BALANCE_F.currency_rk=EXCLUDED.currency_rk
    AND ds.FT_BALANCE_F.balance_out=EXCLUDED.balance_out
);

-- name: CreateBalanceReturn :one
INSERT INTO
    ds.FT_BALANCE_F (on_date, account_rk, currency_rk, balance_out)
VALUES
    ($1, $2, $3, $4)
ON CONFLICT (on_date, account_rk) 
DO UPDATE SET
    currency_rk=EXCLUDED.currency_rk,
    balance_out=EXCLUDED.balance_out
WHERE NOT (
    ds.FT_BALANCE_F.currency_rk=EXCLUDED.currency_rk
    AND ds.FT_BALANCE_F.balance_out=EXCLUDED.balance_out
)
RETURNING *;