# app/repositories/lesson_progress_repository.py
from typing import List, Optional, Tuple, Dict, Any
from app.config.db_config import get_connection

class LessonProgressRepository:
    """
    Repository cho lesson_progress.
    Chỉ tập trung vào truy vấn DB (CRUD), không chứa logic nghiệp vụ.
    """

    def _row_to_dict(self, row) -> Dict[str, Any]:
        return {
            "id": row[0],
            "lesson_id": row[1],
            "user_id": row[2],
            "is_completed": bool(row[3]),
            "completed_at": row[4],
        }

    # ---------- READ ----------
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, lesson_id, user_id, is_completed, completed_at
            FROM lesson_progress
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close(); conn.close()
        return [self._row_to_dict(r) for r in rows]

    def get_by_user_and_lesson(self, user_id: int, lesson_id: int) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, lesson_id, user_id, is_completed, completed_at
            FROM lesson_progress
            WHERE user_id = ? AND lesson_id = ?
            """,
            (user_id, lesson_id),
        )
        row = cursor.fetchone()
        cursor.close(); conn.close()
        return self._row_to_dict(row) if row else None

    # ---------- CREATE ----------
    def create_progress(self, user_id: int, lesson_id: int, is_completed: bool = True) -> int:
        """
        Tạo bản ghi mới. Trả về ID (identity) vừa tạo.
        """
        conn = get_connection()
        cursor = conn.cursor()
        # Nếu hoàn thành ngay thì completed_at = GETDATE()
        if is_completed:
            cursor.execute(
                """
                INSERT INTO lesson_progress (lesson_id, user_id, is_completed, completed_at)
                VALUES (?, ?, 1, GETDATE());
                SELECT SCOPE_IDENTITY();
                """,
                (lesson_id, user_id),
            )
        else:
            cursor.execute(
                """
                INSERT INTO lesson_progress (lesson_id, user_id, is_completed, completed_at)
                VALUES (?, ?, 0, NULL);
                SELECT SCOPE_IDENTITY();
                """,
                (lesson_id, user_id),
            )
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close(); conn.close()
        return int(new_id)

    # ---------- UPDATE ----------
    def update_completion(self, user_id: int, lesson_id: int, is_completed: bool = True) -> int:
        """
        Cập nhật trạng thái hoàn thành theo (user_id, lesson_id).
        Trả về số dòng bị ảnh hưởng.
        """
        conn = get_connection()
        cursor = conn.cursor()
        if is_completed:
            cursor.execute(
                """
                UPDATE lesson_progress
                SET is_completed = 1, completed_at = GETDATE()
                WHERE user_id = ? AND lesson_id = ?
                """,
                (user_id, lesson_id),
            )
        else:
            cursor.execute(
                """
                UPDATE lesson_progress
                SET is_completed = 0, completed_at = NULL
                WHERE user_id = ? AND lesson_id = ?
                """,
                (user_id, lesson_id),
            )
        affected = cursor.rowcount
        conn.commit()
        cursor.close(); conn.close()
        return affected

    # ---------- OPTIONAL: DELETE ----------
    def delete_by_id(self, progress_id: int) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lesson_progress WHERE id = ?", (progress_id,))
        affected = cursor.rowcount
        conn.commit()
        cursor.close(); conn.close()
        return affected

    # ---------- (Tuỳ chọn) Lấy tiến độ theo khóa học ----------
    # Cần bảng lessons(course_id) để join. Nếu bạn chưa có, có thể bỏ qua function này.
    def get_course_progress_raw(self, user_id: int, course_id: int) -> Tuple[int, int]:
        """
        Trả về (total_lessons, completed_lessons) trong 1 khóa học.
        Yêu cầu tồn tại bảng lessons(id, course_id) trong DB Course Service replicate/snapshot
        hoặc view/ETL sang DB đọc. Nếu chưa có, tạm thời mock.
        """
        conn = get_connection()
        cursor = conn.cursor()
        # total lessons
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE course_id = ?", (course_id,))
        total = cursor.fetchone()[0] or 0

        # completed lessons for this user in this course
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM lesson_progress lp
            JOIN lessons l ON l.id = lp.lesson_id
            WHERE lp.user_id = ? AND l.course_id = ? AND lp.is_completed = 1
            """,
            (user_id, course_id),
        )
        completed = cursor.fetchone()[0] or 0

        cursor.close(); conn.close()
        return int(total), int(completed)
