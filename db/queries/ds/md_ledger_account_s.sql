-- name: GetMDLedgerAccount :many
SELECT
    *
FROM
    ds.MD_LEDGER_ACCOUNT_S;


-- name: CreateMDLedgerAccount :exec
INSERT INTO ds.MD_LEDGER_ACCOUNT_S (
    chapter,
    chapter_name,
    section_number,
    section_name,
    subsection_name,
    ledger1_account,
    ledger1_account_name,
    ledger_account,
    ledger_account_name,
    characteristic,
    is_resident,
    is_reserve,
    is_reserved,
    is_loan,
    is_reserved_assets,
    is_overdue,
    is_interest,
    pair_account,
    start_date,
    end_date,
    is_rub_only,
    min_term,
    min_term_measure,
    max_term,
    max_term_measure,
    ledger_acc_full_name_translit,
    is_revaluation,
    is_correct
) VALUES (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    $7,
    $8,
    $9,
    $10,
    $11,
    $12,
    $13,
    $14,
    $15,
    $16,
    $17,
    $18,
    $19,
    $20,
    $21,
    $22,
    $23,
    $24,
    $25,
    $26,
    $27,
    $28
)
ON CONFLICT (ledger_account, start_date)
DO UPDATE SET
    chapter = EXCLUDED.chapter,
    chapter_name = EXCLUDED.chapter_name,
    section_number = EXCLUDED.section_number,
    section_name = EXCLUDED.section_name,
    subsection_name = EXCLUDED.subsection_name,
    ledger1_account = EXCLUDED.ledger1_account,
    ledger1_account_name = EXCLUDED.ledger1_account_name,
    ledger_account_name = EXCLUDED.ledger_account_name,
    characteristic = EXCLUDED.characteristic,
    is_resident = EXCLUDED.is_resident,
    is_reserve = EXCLUDED.is_reserve,
    is_reserved = EXCLUDED.is_reserved,
    is_loan = EXCLUDED.is_loan,
    is_reserved_assets = EXCLUDED.is_reserved_assets,
    is_overdue = EXCLUDED.is_overdue,
    is_interest = EXCLUDED.is_interest,
    pair_account = EXCLUDED.pair_account,
    end_date = EXCLUDED.end_date,
    is_rub_only = EXCLUDED.is_rub_only,
    min_term = EXCLUDED.min_term,
    min_term_measure = EXCLUDED.min_term_measure,
    max_term = EXCLUDED.max_term,
    max_term_measure = EXCLUDED.max_term_measure,
    ledger_acc_full_name_translit = EXCLUDED.ledger_acc_full_name_translit,
    is_revaluation = EXCLUDED.is_revaluation,
    is_correct = EXCLUDED.is_correct
WHERE NOT (
    ds.MD_LEDGER_ACCOUNT_S.chapter = EXCLUDED.chapter
    AND ds.MD_LEDGER_ACCOUNT_S.chapter_name = EXCLUDED.chapter_name
    AND ds.MD_LEDGER_ACCOUNT_S.section_number = EXCLUDED.section_number
    AND ds.MD_LEDGER_ACCOUNT_S.section_name = EXCLUDED.section_name
    AND ds.MD_LEDGER_ACCOUNT_S.subsection_name = EXCLUDED.subsection_name
    AND ds.MD_LEDGER_ACCOUNT_S.ledger1_account = EXCLUDED.ledger1_account
    AND ds.MD_LEDGER_ACCOUNT_S.ledger1_account_name = EXCLUDED.ledger1_account_name
    AND ds.MD_LEDGER_ACCOUNT_S.ledger_account_name = EXCLUDED.ledger_account_name
    AND ds.MD_LEDGER_ACCOUNT_S.characteristic = EXCLUDED.characteristic
    AND ds.MD_LEDGER_ACCOUNT_S.is_resident = EXCLUDED.is_resident
    AND ds.MD_LEDGER_ACCOUNT_S.is_reserve = EXCLUDED.is_reserve
    AND ds.MD_LEDGER_ACCOUNT_S.is_reserved = EXCLUDED.is_reserved
    AND ds.MD_LEDGER_ACCOUNT_S.is_loan = EXCLUDED.is_loan
    AND ds.MD_LEDGER_ACCOUNT_S.is_reserved_assets = EXCLUDED.is_reserved_assets
    AND ds.MD_LEDGER_ACCOUNT_S.is_overdue = EXCLUDED.is_overdue
    AND ds.MD_LEDGER_ACCOUNT_S.is_interest = EXCLUDED.is_interest
    AND ds.MD_LEDGER_ACCOUNT_S.pair_account = EXCLUDED.pair_account
    AND ds.MD_LEDGER_ACCOUNT_S.end_date = EXCLUDED.end_date
    AND ds.MD_LEDGER_ACCOUNT_S.is_rub_only = EXCLUDED.is_rub_only
    AND ds.MD_LEDGER_ACCOUNT_S.min_term = EXCLUDED.min_term
    AND ds.MD_LEDGER_ACCOUNT_S.min_term_measure = EXCLUDED.min_term_measure
    AND ds.MD_LEDGER_ACCOUNT_S.max_term = EXCLUDED.max_term
    AND ds.MD_LEDGER_ACCOUNT_S.max_term_measure = EXCLUDED.max_term_measure
    AND ds.MD_LEDGER_ACCOUNT_S.ledger_acc_full_name_translit = EXCLUDED.ledger_acc_full_name_translit
    AND ds.MD_LEDGER_ACCOUNT_S.is_revaluation = EXCLUDED.is_revaluation
    AND ds.MD_LEDGER_ACCOUNT_S.is_correct = EXCLUDED.is_correct
);


-- name: CreateMDLedgerAccountReturn :one
INSERT INTO ds.MD_LEDGER_ACCOUNT_S (
    chapter,
    chapter_name,
    section_number,
    section_name,
    subsection_name,
    ledger1_account,
    ledger1_account_name,
    ledger_account,
    ledger_account_name,
    characteristic,
    is_resident,
    is_reserve,
    is_reserved,
    is_loan,
    is_reserved_assets,
    is_overdue,
    is_interest,
    pair_account,
    start_date,
    end_date,
    is_rub_only,
    min_term,
    min_term_measure,
    max_term,
    max_term_measure,
    ledger_acc_full_name_translit,
    is_revaluation,
    is_correct
) VALUES (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    $7,
    $8,
    $9,
    $10,
    $11,
    $12,
    $13,
    $14,
    $15,
    $16,
    $17,
    $18,
    $19,
    $20,
    $21,
    $22,
    $23,
    $24,
    $25,
    $26,
    $27,
    $28
)
ON CONFLICT (ledger_account, start_date)
DO UPDATE SET
    chapter = EXCLUDED.chapter,
    chapter_name = EXCLUDED.chapter_name,
    section_number = EXCLUDED.section_number,
    section_name = EXCLUDED.section_name,
    subsection_name = EXCLUDED.subsection_name,
    ledger1_account = EXCLUDED.ledger1_account,
    ledger1_account_name = EXCLUDED.ledger1_account_name,
    ledger_account_name = EXCLUDED.ledger_account_name,
    characteristic = EXCLUDED.characteristic,
    is_resident = EXCLUDED.is_resident,
    is_reserve = EXCLUDED.is_reserve,
    is_reserved = EXCLUDED.is_reserved,
    is_loan = EXCLUDED.is_loan,
    is_reserved_assets = EXCLUDED.is_reserved_assets,
    is_overdue = EXCLUDED.is_overdue,
    is_interest = EXCLUDED.is_interest,
    pair_account = EXCLUDED.pair_account,
    end_date = EXCLUDED.end_date,
    is_rub_only = EXCLUDED.is_rub_only,
    min_term = EXCLUDED.min_term,
    min_term_measure = EXCLUDED.min_term_measure,
    max_term = EXCLUDED.max_term,
    max_term_measure = EXCLUDED.max_term_measure,
    ledger_acc_full_name_translit = EXCLUDED.ledger_acc_full_name_translit,
    is_revaluation = EXCLUDED.is_revaluation,
    is_correct = EXCLUDED.is_correct
WHERE NOT (
    ds.MD_LEDGER_ACCOUNT_S.chapter = EXCLUDED.chapter
    AND ds.MD_LEDGER_ACCOUNT_S.chapter_name = EXCLUDED.chapter_name
    AND ds.MD_LEDGER_ACCOUNT_S.section_number = EXCLUDED.section_number
    AND ds.MD_LEDGER_ACCOUNT_S.section_name = EXCLUDED.section_name
    AND ds.MD_LEDGER_ACCOUNT_S.subsection_name = EXCLUDED.subsection_name
    AND ds.MD_LEDGER_ACCOUNT_S.ledger1_account = EXCLUDED.ledger1_account
    AND ds.MD_LEDGER_ACCOUNT_S.ledger1_account_name = EXCLUDED.ledger1_account_name
    AND ds.MD_LEDGER_ACCOUNT_S.ledger_account_name = EXCLUDED.ledger_account_name
    AND ds.MD_LEDGER_ACCOUNT_S.characteristic = EXCLUDED.characteristic
    AND ds.MD_LEDGER_ACCOUNT_S.is_resident = EXCLUDED.is_resident
    AND ds.MD_LEDGER_ACCOUNT_S.is_reserve = EXCLUDED.is_reserve
    AND ds.MD_LEDGER_ACCOUNT_S.is_reserved = EXCLUDED.is_reserved
    AND ds.MD_LEDGER_ACCOUNT_S.is_loan = EXCLUDED.is_loan
    AND ds.MD_LEDGER_ACCOUNT_S.is_reserved_assets = EXCLUDED.is_reserved_assets
    AND ds.MD_LEDGER_ACCOUNT_S.is_overdue = EXCLUDED.is_overdue
    AND ds.MD_LEDGER_ACCOUNT_S.is_interest = EXCLUDED.is_interest
    AND ds.MD_LEDGER_ACCOUNT_S.pair_account = EXCLUDED.pair_account
    AND ds.MD_LEDGER_ACCOUNT_S.end_date = EXCLUDED.end_date
    AND ds.MD_LEDGER_ACCOUNT_S.is_rub_only = EXCLUDED.is_rub_only
    AND ds.MD_LEDGER_ACCOUNT_S.min_term = EXCLUDED.min_term
    AND ds.MD_LEDGER_ACCOUNT_S.min_term_measure = EXCLUDED.min_term_measure
    AND ds.MD_LEDGER_ACCOUNT_S.max_term = EXCLUDED.max_term
    AND ds.MD_LEDGER_ACCOUNT_S.max_term_measure = EXCLUDED.max_term_measure
    AND ds.MD_LEDGER_ACCOUNT_S.ledger_acc_full_name_translit = EXCLUDED.ledger_acc_full_name_translit
    AND ds.MD_LEDGER_ACCOUNT_S.is_revaluation = EXCLUDED.is_revaluation
    AND ds.MD_LEDGER_ACCOUNT_S.is_correct = EXCLUDED.is_correct
)
RETURNING *;