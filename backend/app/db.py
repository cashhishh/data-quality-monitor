import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=DataQualityDB;"
        "Trusted_Connection=yes;"
        "Connection Timeout=30;"
    )
    return conn
