import json
import pandas as pd

def run_data_quality_checks(records):
    """
    records: list of rows from data_records table (row_data column)
    """

    parsed_rows = [json.loads(r[0]) for r in records]
    df = pd.DataFrame(parsed_rows)

    results = {}

    # 1️⃣ Null value check
    results["null_check"] = int(df.isnull().sum().sum())

    # 2️⃣ Duplicate row check
    results["duplicate_check"] = int(df.duplicated().sum())

    # 3️⃣ Anomaly detection (numeric columns only)
    anomaly_count = 0

    numeric_columns = df.select_dtypes(include="number")

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

    results["anomaly_check"] = int(anomaly_count)

    return results
