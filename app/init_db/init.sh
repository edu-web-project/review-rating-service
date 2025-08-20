#!/bin/bash
# Đợi SQL Server khởi động (khoảng 30 giây)
sleep 30s

# Import file SQL
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "YourStrong(!)Password" -i /docker-entrypoint-initdb.d/progress_service.sql
