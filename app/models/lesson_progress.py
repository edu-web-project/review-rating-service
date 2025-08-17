# app/models/lesson_progress.py
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class LessonProgressCreate(BaseModel):
    """Payload khi tạo/cập nhật tiến độ một bài học."""
    user_id: int = Field(..., description="ID người dùng")
    lesson_id: int = Field(..., description="ID bài học")
    is_completed: bool = Field(default=True, description="Đã hoàn thành hay chưa")

class LessonProgressItem(BaseModel):
    """Bản ghi tiến độ trả về cho client/service khác."""
    id: int
    user_id: int
    lesson_id: int
    is_completed: bool
    completed_at: Optional[datetime] = None

class LessonProgressListResponse(BaseModel):
    """Danh sách tiến độ của user."""
    user_id: int
    items: List[LessonProgressItem]

class CourseProgressResponse(BaseModel):
    """Tiến độ tổng hợp cho 1 khóa (nếu bạn cần)."""
    user_id: int
    course_id: int
    total_lessons: int
    completed_lessons: int
    completion_rate: float  # %
