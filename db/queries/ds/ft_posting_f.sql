-- name: GetPosts :many
SELECT
    *
FROM
    ds.FT_POSTING_F;

-- name: CreatePost :exec
INSERT INTO
    ds.FT_POSTING_F (
        oper_date,
        credit_account_rk,
        debet_account_rk,
        credit_amount,
        debet_amount
    )
VALUES
    ($1, $2, $3, $4, $5);

-- name: CreatePostReturn :one
INSERT INTO
    ds.FT_POSTING_F (
        oper_date,
        credit_account_rk,
        debet_account_rk,
        credit_amount,
        debet_amount
    )
VALUES
    ($1, $2, $3, $4, $5)
RETURNING *;

-- name: TruncatePostingTable :exec
TRUNCATE TABLE ds.FT_POSTING_F;