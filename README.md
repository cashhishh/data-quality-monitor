# Data Quality Monitoring System

A full-stack data quality monitoring platform that allows users to upload datasets, run automated data quality checks, store results in a database, and visualize insights using Power BI.

This project is built to simulate a real-world data engineering + analytics workflow.

---

## 🚀 Features

- Upload datasets (CSV)
- Store dataset metadata in SQL Server
- Run automated data quality checks:
  - Null value detection
  - Duplicate row detection
- Persist validation results in the database
- REST APIs built with FastAPI
- Frontend dashboard for dataset management
- Power BI integration for analytics and visualization
- Synthetic large dataset generation for realistic analysis

---

## 🏗️ Tech Stack

### Backend
- Python
- FastAPI
- SQL Server (ODBC Driver 17)
- Pandas
- PyODBC

### Frontend
- React
- JavaScript
- Axios
- Basic UI components

### Analytics
- Power BI
- SQL Server as data source

---

## 📂 Project Structure

data-quality-monitor/
│
├── backend/
│ ├── app/
│ │ ├── routes/
│ │ ├── services/
│ │ ├── db.py
│ │ └── main.py
│ └── scripts/
│ └── generate_synthetic_data.py
│
├── frontend/
│
├── .gitignore
├── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/cashhishh/data-quality-monitor.git
cd data-quality-monitor

2️⃣ Backend setup
cd backend
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt


Update database connection in app/db.py:

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=DataQualityDB;"
        "Trusted_Connection=yes;"
    )


Run backend:

uvicorn app.main:app --reload


API Docs available at:

http://127.0.0.1:8000/docs

3️⃣ Frontend setup
cd frontend
npm install
npm start

📊 Power BI Integration

Connect Power BI to SQL Server

Use tables:

datasets

dataset_records

validation_results

Build visuals such as:

Dataset count

Null percentage

Duplicate rows

Upload trends over time

🧪 Synthetic Data

To generate large datasets for realistic analysis:

python backend/scripts/generate_synthetic_data.py


This helps simulate real-world data volumes instead of small demo files.

🔮 Future Enhancements

Column-level data quality rules

Schema validation

Data freshness checks

Scheduled quality checks

Authentication & user roles

Cloud deployment (Docker + Azure/AWS)

📌 Why this project?

This project demonstrates:

Backend API design

Database integration

Data quality concepts

Analytics + visualization

End-to-end data pipeline thinking

👩‍💻 Author

Kashish
B.Tech ECE | Data & Software Enthusiast

