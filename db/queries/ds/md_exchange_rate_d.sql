-- name: GetMDExchangeRate :many
SELECT
    *
FROM
    ds.MD_EXCHANGE_RATE_D;


-- name: CreateMDExchangeRate :exec
INSERT INTO ds.MD_EXCHANGE_RATE_D (
    data_actual_date,
    data_actual_end_date,
    currency_rk,
    reduced_cource,
    code_iso_num
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
    reduced_cource=EXCLUDED.reduced_cource,
    code_iso_num=EXCLUDED.code_iso_num
WHERE NOT (
    ds.MD_EXCHANGE_RATE_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_EXCHANGE_RATE_D.reduced_cource=EXCLUDED.reduced_cource
    AND ds.MD_EXCHANGE_RATE_D.code_iso_num=EXCLUDED.code_iso_num
);



-- name: CreateMDExchangeRateReturn :one
INSERT INTO ds.MD_EXCHANGE_RATE_D (
    data_actual_date,
    data_actual_end_date,
    currency_rk,
    reduced_cource,
    code_iso_num
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
    reduced_cource=EXCLUDED.reduced_cource,
    code_iso_num=EXCLUDED.code_iso_num
WHERE NOT (
    ds.MD_EXCHANGE_RATE_D.data_actual_end_date=EXCLUDED.data_actual_end_date
    AND ds.MD_EXCHANGE_RATE_D.reduced_cource=EXCLUDED.reduced_cource
    AND ds.MD_EXCHANGE_RATE_D.code_iso_num=EXCLUDED.code_iso_num
)
RETURNING *;