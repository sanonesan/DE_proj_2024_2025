-- name: GetMDAccounts :many
SELECT
    *
FROM
    ds.MD_ACCOUNT_D;


-- name: CreateMDAccount :exec
INSERT INTO
    ds.MD_ACCOUNT_D (
        data_actual_date,
        data_actual_end_date,
        account_rk,
        account_number,
        char_type,
        currency_rk,
        currency_code
    )
VALUES
    (
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7
    )
ON CONFLICT (data_actual_date, account_rk) 
DO UPDATE SET
    data_actual_end_date=EXCLUDED.data_actual_end_date,
    account_number=EXCLUDED.account_number,
    char_type=EXCLUDED.char_type,    
    currency_rk=EXCLUDED.currency_rk,
    currency_code=EXCLUDED.currency_code
WHERE NOT (
    ds.MD_ACCOUNT_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_ACCOUNT_D.account_number=EXCLUDED.account_number
    AND ds.MD_ACCOUNT_D.char_type=EXCLUDED.char_type
    AND ds.MD_ACCOUNT_D.currency_rk=EXCLUDED.currency_rk
    AND ds.MD_ACCOUNT_D.currency_code=EXCLUDED.currency_code
);

-- name: CreateMDAccountReturn :one
INSERT INTO
    ds.MD_ACCOUNT_D (
        data_actual_date,
        data_actual_end_date,
        account_rk,
        account_number,
        char_type,
        currency_rk,
        currency_code
    )
VALUES
    (
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7
    )
ON CONFLICT (data_actual_date, account_rk) 
DO UPDATE SET
    data_actual_end_date=EXCLUDED.data_actual_end_date,
    account_number=EXCLUDED.account_number,
    char_type=EXCLUDED.char_type,    
    currency_rk=EXCLUDED.currency_rk,
    currency_code=EXCLUDED.currency_code
WHERE NOT (
    ds.MD_ACCOUNT_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_ACCOUNT_D.account_number=EXCLUDED.account_number
    AND ds.MD_ACCOUNT_D.char_type=EXCLUDED.char_type
    AND ds.MD_ACCOUNT_D.currency_rk=EXCLUDED.currency_rk
    AND ds.MD_ACCOUNT_D.currency_code=EXCLUDED.currency_code
)
RETURNING *;