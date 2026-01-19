import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=DataQualityDB;"
        "Trusted_Connection=yes;",
        timeout=5
    )
    return conn
