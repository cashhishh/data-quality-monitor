from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.dataset_routes import router as dataset_router
from app.routes.dashboard_routes import router as dashboard_router
from app.db import get_connection, init_db


# ✅ CREATE APP FIRST
app = FastAPI(title="Data Quality Monitoring System")

# ✅ ADD CORS AFTER app IS CREATED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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
        return {"db_status": "connected"}
    except Exception as e:
        return {"db_status": "failed", "error": str(e)}

@app.on_event("startup")
def startup_event():
    init_db()
