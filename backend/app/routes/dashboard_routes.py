from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1️⃣ total datasets
        cursor.execute("SELECT COUNT(*) FROM datasets")
        total_datasets = cursor.fetchone()[0]

        # 2️⃣ total checks run
        cursor.execute("SELECT COUNT(*) FROM validation_results")
        total_checks = cursor.fetchone()[0]

        # 3️⃣ failed checks (issue_count > 0)
        cursor.execute("""
            SELECT COUNT(*)
            FROM validation_results
            WHERE issue_count > 0
        """)
        failed_checks = cursor.fetchone()[0]

        # 4️⃣ average quality score per dataset
        cursor.execute("""
            SELECT dataset_id,
                   SUM(CASE WHEN issue_count = 0 THEN 1 ELSE 0 END) * 100.0
                   / COUNT(*) AS score
            FROM validation_results
            GROUP BY dataset_id
        """)

        scores = cursor.fetchall()
        avg_score = (
            int(sum(row[1] for row in scores) / len(scores))
            if scores else 0
        )

        return {
            "total_datasets": total_datasets,
            "total_checks": total_checks,
            "failed_checks": failed_checks,
            "average_quality_score": avg_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if conn:
            conn.close()
