from fastapi import APIRouter, UploadFile, File, HTTPException
from app.db import get_connection
from app.services.validation_service import run_data_quality_checks
import pandas as pd
import json

router = APIRouter(prefix="/datasets", tags=["Datasets"])


# ---------------------------
# Health Check
# ---------------------------
@router.get("/health")
def health_check():
    return {"status": "Dataset routes working"}


# ---------------------------
# Create Dataset (metadata only)
# ---------------------------
@router.post("/create")
def create_dataset(dataset_name: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO datasets (dataset_name)
            VALUES (%s)
            RETURNING dataset_id
            """,
            (dataset_name,)
        )

        dataset_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Dataset created",
            "dataset_id": dataset_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Upload Dataset (CSV)
# ---------------------------
@router.post("/upload")
def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        df = pd.read_csv(file.file)

        conn = get_connection()
        cursor = conn.cursor()

        # create dataset entry
        cursor.execute(
            """
            INSERT INTO datasets (dataset_name)
            VALUES (%s)
            RETURNING dataset_id
            """,
            (file.filename,)
        )

        dataset_id = cursor.fetchone()[0]

        # insert rows
        for _, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO data_records (dataset_id, row_data)
                VALUES (%s, %s)
                """,
                (dataset_id, json.dumps(row.to_dict()))
            )

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Dataset uploaded successfully",
            "dataset_id": dataset_id,
            "total_rows": len(df)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Run Data Quality Checks
# ---------------------------
@router.post("/run-checks/{dataset_id}")
def run_checks(dataset_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT row_data FROM data_records WHERE dataset_id = %s",
            (dataset_id,)
        )
        records = cursor.fetchall()

        if not records:
            raise HTTPException(status_code=404, detail="No records found")

        raw_results = run_data_quality_checks(records)

        checks = []
        failed = 0
        total = len(raw_results)

        for check_type, issue_count in raw_results.items():
            status = "PASS" if issue_count == 0 else "FAIL"
            if status == "FAIL":
                failed += 1

            checks.append({
                "check_name": check_type.replace("_", " ").upper(),
                "status": status,
                "failed_rows": issue_count
            })

            cursor.execute(
                """
                INSERT INTO validation_results (dataset_id, check_type, issue_count)
                VALUES (%s, %s, %s)
                """,
                (dataset_id, check_type, issue_count)
            )

        overall_score = int(((total - failed) / total) * 100)

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "dataset_id": dataset_id,
            "overall_score": overall_score,
            "checks": checks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Get Latest Dataset ID
# ---------------------------
@router.get("/latest")
def get_latest_dataset():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT dataset_id
            FROM datasets
            ORDER BY dataset_id DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        return {"dataset_id": row[0] if row else None}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
