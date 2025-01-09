-- Создание пользователя "ds_user"
CREATE USER ds_user
WITH
    PASSWORD 'ds_pwd';

-- Replace 'your_password' with a strong password
-- Создание схемы "ds"
CREATE SCHEMA ds AUTHORIZATION ds_user;

-- Предоставление прав пользователю на схему
GRANT USAGE ON SCHEMA ds TO ds_user;

-- Установка схемы ds по умолчанию для пользователя ds_user
ALTER USER ds_user
SET
    search_path TO ds;











