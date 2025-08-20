# Base image Python
FROM python:3.10-slim

# Cài đặt các thư viện hệ thống cần cho pyodbc + SQL Server ODBC Driver
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++ \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Microsoft ODBC Driver for SQL Server (msodbcsql17)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Chạy FastAPI bằng Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
