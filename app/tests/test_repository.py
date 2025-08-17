from repositories.progress_repository import LessonProgressRepository

def test_get_all():
    repo = LessonProgressRepository()
    progress_list = repo.add_progress()

    print("=== Kết quả lấy dữ liệu từ bảng lesson_progress ===")
    for row in progress_list:
        print(row)

if __name__ == "__main__":
    test_get_all()
