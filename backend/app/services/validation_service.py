import pandas as pd
import logging

logger = logging.getLogger(__name__)


def run_data_quality_checks(records):
    """
    Run data quality checks on records from PostgreSQL JSONB column.
    
    Args:
        records: List of tuples from query "SELECT row_data FROM data_records"
                 where row_data is JSONB (auto-decoded to Python dict by psycopg2)
    
    Returns:
        dict: Results of quality checks {check_name: issue_count}
    """
    
    # ✅ psycopg2 already decodes JSONB to Python dicts - NO json.loads needed!
    parsed_rows = [r[0] for r in records]
    
    if not parsed_rows:
        logger.warning("⚠️ No records to validate")
        return {
            "null_check": 0,
            "duplicate_check": 0,
            "anomaly_check": 0
        }
    
    logger.info(f"🔍 Running quality checks on {len(parsed_rows)} records...")
    
    try:
        df = pd.DataFrame(parsed_rows)
        logger.info(f"📊 DataFrame created: {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        logger.error(f"❌ Failed to create DataFrame: {str(e)}")
        raise
    
    results = {}

    # 1️⃣ Null value check
    null_count = int(df.isnull().sum().sum())
    results["null_check"] = null_count
    logger.info(f"  ✓ Null check: {null_count} null values found")

    # 2️⃣ Duplicate row check
    duplicate_count = int(df.duplicated().sum())
    results["duplicate_check"] = duplicate_count
    logger.info(f"  ✓ Duplicate check: {duplicate_count} duplicate rows found")

    # 3️⃣ Anomaly detection (numeric columns only)
    anomaly_count = 0
    numeric_columns = df.select_dtypes(include="number")
    
    if len(numeric_columns.columns) > 0:
        logger.info(f"  🔢 Checking {len(numeric_columns.columns)} numeric columns for anomalies...")
        
        for col in numeric_columns.columns:
            mean = numeric_columns[col].mean()
            std = numeric_columns[col].std()

            if pd.isna(std) or std == 0:
                continue

            lower_bound = mean - 3 * std
            upper_bound = mean + 3 * std

            anomalies = numeric_columns[
                (numeric_columns[col] < lower_bound) |
                (numeric_columns[col] > upper_bound)
            ]

            anomaly_count += len(anomalies)
    else:
        logger.info("  ⚠️ No numeric columns found for anomaly detection")
    
    results["anomaly_check"] = int(anomaly_count)
    logger.info(f"  ✓ Anomaly check: {anomaly_count} anomalies found")
    
    logger.info(f"✅ Quality checks completed: {results}")

    return results
