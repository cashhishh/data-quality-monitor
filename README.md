# 📊 Data Quality Monitoring System

A full-stack **Data Quality Monitoring System** that allows users to upload datasets, run automated data quality checks, and visualize results through an interactive dashboard.

Built with **FastAPI + PostgreSQL + React (Vite)** and deployed on **Render + Netlify**.

---

## 🚀 Live Demo

- **Frontend (Netlify):**  
  https://dataquality-monitor.netlify.app/

- **Backend API (Render):**  
  https://data-quality-monitor-1.onrender.com/

---

## 🧠 Features

### ✅ Dataset Management
- Upload CSV datasets
- Automatically store raw rows in PostgreSQL (`JSONB`)
- Fetch latest uploaded dataset

### ✅ Data Quality Checks
- Null value detection
- Duplicate record detection
- Simple anomaly detection
- Overall quality score calculation

### ✅ Dashboard
- Visual summary of data quality results
- Pass / Fail status per check
- Aggregated metrics for latest dataset

### ✅ Production-Ready Backend
- PostgreSQL with JSONB storage
- Automatic table creation on startup
- Robust error handling
- Detailed logging (Render-friendly)
- CORS configured for Netlify

---

## 🏗️ Tech Stack

### Frontend
- React (Vite)
- JavaScript
- Fetch API
- Netlify (Deployment)

### Backend
- FastAPI
- psycopg2 (PostgreSQL)
- Pandas (CSV processing)
- Uvicorn (ASGI server)
- Render (Deployment)

### Database
- PostgreSQL (Render)
- JSONB for flexible row storage

---

---

## 🔌 API Endpoints

### Health & DB
- `GET /` → API status
- `GET /db-test` → Database connectivity check

### Datasets
- `POST /datasets/upload` → Upload CSV file
- `GET /datasets/latest` → Get latest dataset ID
- `POST /datasets/run-checks/{dataset_id}` → Run quality checks

### Dashboard
- `GET /dashboard/summary` → Aggregated quality metrics

---

## 🧪 Example Flow

1. Upload a CSV dataset from frontend
2. Dataset is stored in PostgreSQL (JSONB)
3. Run quality checks
4. View:
   - Overall quality score
   - Individual check results
   - Dashboard visualizations

---

