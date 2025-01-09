-- Создание пользователя "logs_user"
CREATE USER logs_user
WITH
    PASSWORD 'logs_pass';

-- Replace 'your_password' with a strong password

-- Создание схемы "logs"
CREATE SCHEMA logs AUTHORIZATION logs_user;

-- Предоставление прав пользователю на схему
GRANT USAGE ON SCHEMA logs TO logs_user;

-- Создание таблицы "application_logs" в схеме "logs"
CREATE TABLE
    logs.application_logs (
        log_id SERIAL PRIMARY KEY,
        application_name VARCHAR(255),
        log_timestamp TIMESTAMP WITH TIME ZONE,
        log_level VARCHAR(10), 
        log_message TEXT
    );

-- Предоставление прав пользователю на таблицу
GRANT SELECT, INSERT, UPDATE, DELETE ON logs.application_logs TO logs_user;

-- Предоставление прав пользователю на последовательность (для log_id SERIAL)
GRANT USAGE, SELECT ON SEQUENCE logs.application_logs_log_id_seq TO logs_user;