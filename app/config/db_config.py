import os
import pyodbc

def get_connection():
    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_NAME", "ProgressService")
    username = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD", "YourStrong(!)Password")

    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    return conn
