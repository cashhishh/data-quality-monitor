import os
import psycopg2
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    """Get a raw database connection."""
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is not set")
    
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@contextmanager
def get_db():
    """
    Context manager for database connections.
    Ensures proper cleanup even on errors.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def init_db():
    """
    Initialize database tables on startup.
    Safe to run multiple times (uses IF NOT EXISTS).
    """
    logger.info("🔧 Initializing database tables...")
    
    try:
        with get_db() as cursor:
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
            
            logger.info("✅ Database tables initialized successfully")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {str(e)}")
        raise
