from fastapi import APIRouter, UploadFile, File, HTTPException
from app.db import get_connection
import pandas as pd
import json

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("/health")
def health_check():
    return {"status": "Dataset routes working"}


@router.post("/create")
def create_dataset(dataset_name: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO datasets (dataset_name)
            OUTPUT INSERTED.dataset_id
            VALUES (?)
            """,
            dataset_name
        )

        dataset_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "message": "Dataset created",
            "dataset_id": int(dataset_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        # Read CSV
        df = pd.read_csv(file.file)

        conn = get_connection()
        cursor = conn.cursor()

        # Insert dataset
        cursor.execute(
            """
            INSERT INTO datasets (dataset_name)
            OUTPUT INSERTED.dataset_id
            VALUES (?)
            """,
            file.filename
        )

        dataset_id = cursor.fetchone()[0]

        # Insert rows
        for _, row in df.iterrows():
            row_json = json.dumps(row.to_dict())

            cursor.execute(
                """
                INSERT INTO data_records (dataset_id, row_data)
                VALUES (?, ?)
                """,
                dataset_id,
                row_json
            )

        conn.commit()

        return {
            "message": "Dataset uploaded successfully",
            "dataset_id": int(dataset_id),
            "total_rows": len(df)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.services.validation_service import run_data_quality_checks


@router.post("/run-checks/{dataset_id}")
def _run_checks_sync(dataset_id: int):
    print("STEP 1: Endpoint hit")

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("STEP 2: DB connection acquired")

        cursor.execute(
            "SELECT row_data FROM data_records WHERE dataset_id = ?",
            dataset_id
        )
        records = cursor.fetchall()
        print(f"STEP 3: Fetched {len(records)} records")

        if not records:
            return {"message": "No records found"}

        print("STEP 4: Starting data quality checks")
        results = run_data_quality_checks(records)
        print("STEP 5: Checks completed")

        for check_type, issue_count in results.items():
            cursor.execute(
                """
                INSERT INTO validation_results (dataset_id, check_type, issue_count)
                VALUES (?, ?, ?)
                """,
                dataset_id,
                check_type,
                issue_count
            )

        conn.commit()
        print("STEP 6: Results committed")

        return {
            "dataset_id": dataset_id,
            "results": results
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()
            print("STEP 7: DB connection closed")
