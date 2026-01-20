from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.dataset_routes import router as dataset_router
from app.routes.dashboard_routes import router as dashboard_router
from app.db import get_connection, init_db

# ✅ CREATE APP FIRST
app = FastAPI(title="Data Quality Monitoring System")

# ✅ RUN DB INIT ON STARTUP (AUTO-CREATE TABLES)
@app.on_event("startup")
def startup_event():
    init_db()

# ✅ CORS (ALLOW NETLIFY + LOCAL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://dataquality-monitor.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(dataset_router)
app.include_router(dashboard_router)

# ✅ ROOT
@app.get("/")
def root():
    return {"status": "API is running"}

# ✅ DB TEST
@app.get("/db-test")
def db_test():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return {"db_status": "connected"}
    except Exception as e:
        return {"db_status": "failed", "error": str(e)}
