from fastapi import APIRouter, UploadFile, File, HTTPException
from app.db import get_connection, get_db
from app.services.validation_service import run_data_quality_checks
import pandas as pd
import json
import logging
import io

logger = logging.getLogger(__name__)

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
        with get_db() as cursor:
            cursor.execute(
                """
                INSERT INTO datasets (dataset_name)
                VALUES (%s)
                RETURNING dataset_id
                """,
                (dataset_name,)
            )
            dataset_id = cursor.fetchone()[0]
        
        return {
            "message": "Dataset created",
            "dataset_id": dataset_id
        }
    
    except Exception as e:
        logger.error(f"Failed to create dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Upload Dataset (CSV)
# ---------------------------
@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    logger.info(f"📤 Upload started: {file.filename}")
    
    # Validate file extension
    if not file.filename.endswith(".csv"):
        logger.warning(f"❌ Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    dataset_id = None
    total_rows = 0
    
    try:
        # Read CSV file content
        logger.info("📖 Reading CSV file...")
        content = await file.read()
        
        # Parse CSV with error handling
        try:
            df = pd.read_csv(io.BytesIO(content), encoding='utf-8')
        except UnicodeDecodeError:
            # Try alternative encoding
            df = pd.read_csv(io.BytesIO(content), encoding='latin-1')
        
        total_rows = len(df)
        logger.info(f"✅ CSV parsed successfully: {total_rows} rows, {len(df.columns)} columns")
        
        if total_rows == 0:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Insert into database using context manager
        with get_db() as cursor:
            # Create dataset entry
            logger.info("💾 Creating dataset entry...")
            cursor.execute(
                """
                INSERT INTO datasets (dataset_name)
                VALUES (%s)
                RETURNING dataset_id
                """,
                (file.filename,)
            )
            dataset_id = cursor.fetchone()[0]
            logger.info(f"✅ Dataset created with ID: {dataset_id}")
            
            # Insert rows in batches for better performance
            logger.info(f"💾 Inserting {total_rows} rows...")
            batch_size = 500
            rows_inserted = 0
            
            for i in range(0, total_rows, batch_size):
                batch = df.iloc[i:i+batch_size]
                for _, row in batch.iterrows():
                    # Convert row to JSON, handling NaN values
                    row_dict = row.to_dict()
                    # Replace NaN with None for JSON serialization
                    row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
                    
                    cursor.execute(
                        """
                        INSERT INTO data_records (dataset_id, row_data)
                        VALUES (%s, %s)
                        """,
                        (dataset_id, json.dumps(row_dict))
                    )
                    rows_inserted += 1
                
                logger.info(f"  📊 Progress: {rows_inserted}/{total_rows} rows inserted")
        
        logger.info(f"✅ Upload completed successfully: dataset_id={dataset_id}, rows={total_rows}")
        
        return {
            "message": "Dataset uploaded successfully",
            "dataset_id": dataset_id,
            "total_rows": total_rows,
            "columns": list(df.columns)
        }
    
    except pd.errors.EmptyDataError:
        logger.error("❌ CSV file is empty or malformed")
        raise HTTPException(status_code=400, detail="CSV file is empty or malformed")
    
    except pd.errors.ParserError as e:
        logger.error(f"❌ CSV parsing error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Upload failed: {str(e)}"
        )


# ---------------------------
# Run Data Quality Checks
# ---------------------------
@router.post("/run-checks/{dataset_id}")
def run_checks(dataset_id: int):
    try:
        with get_db() as cursor:
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
            
            overall_score = int(((total - failed) / total) * 100) if total > 0 else 0
        
        return {
            "dataset_id": dataset_id,
            "overall_score": overall_score,
            "checks": checks
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to run checks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Get Latest Dataset ID
# ---------------------------
@router.get("/latest")
def get_latest_dataset():
    try:
        with get_db() as cursor:
            cursor.execute(
                """
                SELECT dataset_id
                FROM datasets
                ORDER BY dataset_id DESC
                LIMIT 1
                """
            )
            row = cursor.fetchone()
        
        return {"dataset_id": row[0] if row else None}
    
    except Exception as e:
        logger.error(f"Failed to get latest dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
