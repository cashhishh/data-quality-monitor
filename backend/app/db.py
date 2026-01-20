import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is not set")

    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # datasets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            dataset_id SERIAL PRIMARY KEY,
            dataset_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # data_records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_records (
            record_id SERIAL PRIMARY KEY,
            dataset_id INTEGER REFERENCES datasets(dataset_id) ON DELETE CASCADE,
            row_data JSONB NOT NULL
        );
    """)

    # validation_results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validation_results (
            result_id SERIAL PRIMARY KEY,
            dataset_id INTEGER REFERENCES datasets(dataset_id) ON DELETE CASCADE,
            check_type TEXT NOT NULL,
            issue_count INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
