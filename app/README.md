# Progress Service

Progress Service là một microservice trong hệ thống học trực tuyến, chịu trách nhiệm quản lý tiến độ học tập của người dùng cho từng bài học.

## 📌 Chức năng chính
- Lưu lại tiến độ hoàn thành bài học của người dùng
- Đánh dấu bài học là hoàn thành / chưa hoàn thành
- Lấy danh sách tiến độ học tập theo người dùng hoặc khóa học
- Kết nối với các service khác (Course Service, User Service)

## 🏗️ Kiến trúc
Service này được xây dựng bằng:
- **Python 3.11+**
- **FastAPI** làm framework API
- **SQL Server** để lưu dữ liệu
- **PyODBC** để kết nối cơ sở dữ liệu
- Mô hình **MVC + Repository Pattern** đơn giản

## 📂 Cấu trúc thư mục 8/12
progress_service/
│── app/
│ ├── controllers/ # Xử lý request/response
│ ├── services/ # Xử lý logic nghiệp vụ
│ ├── repositories/ # Tương tác DB
│ ├── models/ # Định nghĩa schema (Pydantic)
│── config/
│ ├── db_config.py # Cấu hình kết nối DB
│── requirements.txt # Thư viện cần cài
│── README.md # Tài liệu dự án