DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'etl_proj_db') THEN
        CREATE DATABASE etl_proj_db;
    END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE etl_proj_db to postgres;