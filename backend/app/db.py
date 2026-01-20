import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            dataset_id SERIAL PRIMARY KEY,
            dataset_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_records (
            record_id SERIAL PRIMARY KEY,
            dataset_id INTEGER REFERENCES datasets(dataset_id),
            row_data JSONB
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validation_results (
            result_id SERIAL PRIMARY KEY,
            dataset_id INTEGER REFERENCES datasets(dataset_id),
            check_type TEXT,
            issue_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
