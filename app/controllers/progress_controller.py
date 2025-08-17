# app/controllers/progress_controller.py
from fastapi import APIRouter, HTTPException
from app.services.progress_service import LessonProgressService
from app.models.lesson_progress import (
    LessonProgressCreate,
    LessonProgressListResponse,
    LessonProgressItem,
    CourseProgressResponse,
)

router = APIRouter(prefix="/progress", tags=["progress"])
service = LessonProgressService()

@router.get("/user/{user_id}", response_model=LessonProgressListResponse)
def get_user_progress(user_id: int):
    return service.get_user_progress(user_id)

@router.get("/user/{user_id}/lesson/{lesson_id}", response_model=LessonProgressItem)
def get_user_lesson_progress(user_id: int, lesson_id: int):
    item = service.get_user_lesson_progress(user_id, lesson_id)
    if not item:
        raise HTTPException(status_code=404, detail="Progress not found")
    return item

@router.post("/upsert", response_model=LessonProgressItem)
def upsert_progress(payload: LessonProgressCreate):
    return service.upsert_lesson_progress(payload)

@router.post("/complete", response_model=LessonProgressItem)
def mark_complete(payload: LessonProgressCreate):
    # chỉ cần user_id + lesson_id, is_completed bỏ qua
    return service.mark_complete(payload.user_id, payload.lesson_id)

@router.post("/uncomplete", response_model=LessonProgressItem)
def unmark_complete(payload: LessonProgressCreate):
    return service.unmark_complete(payload.user_id, payload.lesson_id)

# Tuỳ chọn: tổng hợp theo khóa (nếu có bảng lessons)
@router.get("/user/{user_id}/course/{course_id}", response_model=CourseProgressResponse)
def course_progress(user_id: int, course_id: int):
    return service.get_course_progress(user_id, course_id)
