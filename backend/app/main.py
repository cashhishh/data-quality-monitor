from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.routes.dataset_routes import router as dataset_router
from app.routes.dashboard_routes import router as dashboard_router


app = FastAPI(title="Data Quality Monitoring System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dataset_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"status": "API is running"}

from app.db import get_connection

@app.get("/db-test")
def db_test():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        return {"db_status": "connected"}
    except Exception as e:
        return {"db_status": "failed", "error": str(e)}
