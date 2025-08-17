import pyodbc  # thư viện kết nối SQL Server qua ODBC

# Thông tin kết nối
server = 'ADMIN-PC'                # hoặc tên server SQL
database = 'progress_service'      # tên database
username = 'thaian'                # user SQL Server
password = '080324'                # mật khẩu

# Hàm trả về connection
def get_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    return pyodbc.connect(connection_string)
