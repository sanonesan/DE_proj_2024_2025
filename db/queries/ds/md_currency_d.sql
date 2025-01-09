-- name: GetMDCurrency :many
SELECT
    *
FROM
    ds.MD_CURRENCY_D;


-- name: CreateMDCurrency :exec
INSERT INTO ds.MD_CURRENCY_D (
    currency_rk,
    data_actual_date,
    data_actual_end_date,
    currency_code,
    code_iso_char
) VALUES (
    $1,
    $2,
    $3,
    $4,
    $5
)
ON CONFLICT (data_actual_date, currency_rk) 
DO UPDATE SET
    data_actual_end_date=EXCLUDED.data_actual_end_date,
    currency_code=EXCLUDED.currency_code,
    code_iso_char=EXCLUDED.code_iso_char
WHERE NOT (
    ds.MD_CURRENCY_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_CURRENCY_D.currency_code=EXCLUDED.currency_code
    AND ds.MD_CURRENCY_D.code_iso_char=EXCLUDED.code_iso_char
);


-- name: CreateMDCurrencyReturn :one
INSERT INTO ds.MD_CURRENCY_D (
    currency_rk,
    data_actual_date,
    data_actual_end_date,
    currency_code,
    code_iso_char
) VALUES (
    $1,
    $2,
    $3,
    $4,
    $5
)
ON CONFLICT (data_actual_date, currency_rk) 
DO UPDATE SET
    data_actual_end_date=EXCLUDED.data_actual_end_date,
    currency_code=EXCLUDED.currency_code,
    code_iso_char=EXCLUDED.code_iso_char
WHERE NOT (
    ds.MD_CURRENCY_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_CURRENCY_D.currency_code=EXCLUDED.currency_code
    AND ds.MD_CURRENCY_D.code_iso_char=EXCLUDED.code_iso_char
)
RETURNING *;