-- name: GetLogs :many
SELECT 
    *
FROM 
    logs.application_logs;


-- name: CreateLog :exec
INSERT INTO logs.application_logs (
    application_name,
    log_timestamp,
    log_level,
    log_message
) VALUES (
    $1,
    $2,
    $3,
    $4
);