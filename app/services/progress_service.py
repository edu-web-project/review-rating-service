# app/services/lesson_progress_service.py
from typing import List, Optional
from app.repositories.progress_repository import LessonProgressRepository
from app.models.lesson_progress import (
    LessonProgressCreate,
    LessonProgressItem,
    LessonProgressListResponse,
    CourseProgressResponse,
)

class LessonProgressService:
    """
    Service layer: chứa logic nghiệp vụ.
    - Tránh trùng record (user_id, lesson_id)
    - Cho phép đánh dấu hoàn thành / bỏ hoàn thành
    - Tổng hợp tiến độ theo user, theo khóa
    """

    def __init__(self):
        self.repo = LessonProgressRepository()

    # ------- Query cơ bản -------
    def get_user_progress(self, user_id: int) -> LessonProgressListResponse:
        rows = self.repo.get_by_user_id(user_id)
        items = [LessonProgressItem(**r) for r in rows]
        return LessonProgressListResponse(user_id=user_id, items=items)

    def get_user_lesson_progress(self, user_id: int, lesson_id: int) -> Optional[LessonProgressItem]:
        row = self.repo.get_by_user_and_lesson(user_id, lesson_id)
        return LessonProgressItem(**row) if row else None

    # ------- Tạo/Cập nhật -------
    def upsert_lesson_progress(self, payload: LessonProgressCreate) -> LessonProgressItem:
        """
        Nếu đã có record (user_id, lesson_id) -> update
        Nếu chưa có -> create
        """
        existing = self.repo.get_by_user_and_lesson(payload.user_id, payload.lesson_id)
        if existing:
            self.repo.update_completion(payload.user_id, payload.lesson_id, payload.is_completed)
            updated = self.repo.get_by_user_and_lesson(payload.user_id, payload.lesson_id)
            return LessonProgressItem(**updated)
        else:
            new_id = self.repo.create_progress(
                user_id=payload.user_id,
                lesson_id=payload.lesson_id,
                is_completed=payload.is_completed,
            )
            # lấy lại bản ghi vừa tạo
            created = self.repo.get_by_user_and_lesson(payload.user_id, payload.lesson_id)
            return LessonProgressItem(**created)

    def mark_complete(self, user_id: int, lesson_id: int) -> LessonProgressItem:
        self.repo.update_completion(user_id, lesson_id, True)
        row = self.repo.get_by_user_and_lesson(user_id, lesson_id)
        # nếu chưa có record (update không đổi dòng nào), tạo mới:
        if not row:
            self.repo.create_progress(user_id, lesson_id, True)
            row = self.repo.get_by_user_and_lesson(user_id, lesson_id)
        return LessonProgressItem(**row)

    def unmark_complete(self, user_id: int, lesson_id: int) -> LessonProgressItem:
        self.repo.update_completion(user_id, lesson_id, False)
        row = self.repo.get_by_user_and_lesson(user_id, lesson_id)
        if not row:
            # Nếu business không cho phép tồn tại record chưa completed thì có thể create với False
            self.repo.create_progress(user_id, lesson_id, False)
            row = self.repo.get_by_user_and_lesson(user_id, lesson_id)
        return LessonProgressItem(**row)

    # ------- Tổng hợp theo khóa (tuỳ chọn nếu đã có bảng lessons) -------
    def get_course_progress(self, user_id: int, course_id: int) -> CourseProgressResponse:
        total, completed = self.repo.get_course_progress_raw(user_id, course_id)
        rate = 0.0 if total == 0 else round(completed / total * 100, 2)
        return CourseProgressResponse(
            user_id=user_id,
            course_id=course_id,
            total_lessons=total,
            completed_lessons=completed,
            completion_rate=rate,
        )
