from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlite3 import Cursor

from student_journal.adapters.converter import lesson_retort, lesson_to_list_retort
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.exceptions.lesson import LessonDoesNotExistError
from student_journal.application.models.lesson import LessonsByDate, WeekLessons
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId


@dataclass(slots=True, frozen=True)
class SQLiteLessonGateway(LessonGateway):
    cursor: Cursor

    def read_lesson(self, lesson_id: LessonId) -> Lesson:
        query = """
            SELECT lesson_id, subject_id, at, mark, note, room, index_number
            FROM Lesson WHERE lesson_id = ?
            """
        res = self.cursor.execute(query, (str(lesson_id),)).fetchone()

        if not res:
            raise LessonDoesNotExistError

        lesson = lesson_retort.load(res, Lesson)

        return lesson

    def write_lesson(self, lesson: Lesson) -> None:
        query = """
            INSERT INTO Lesson
            (lesson_id, subject_id, at, mark, note, room, index_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        params = lesson_to_list_retort.dump(lesson)
        self.cursor.execute(query, params)

    def update_lesson(self, lesson: Lesson) -> None:
        query = """
            UPDATE Lesson SET
            subject_id = ?, at = ?, mark = ?, note = ?, room = ?, index_number = ?
            WHERE lesson_id = ?
            """
        params = lesson_to_list_retort.dump(lesson)
        params.append(params.pop(0))

        self.cursor.execute(query, params)

    def delete_lesson(self, lesson_id: LessonId) -> None:
        query = """
            DELETE FROM Lesson
            WHERE lesson_id = ?
            """
        self.cursor.execute(query, (str(lesson_id),))

    def read_lessons_for_week(self, week_start: datetime) -> WeekLessons:
        query = """
            SELECT * FROM Lesson
            WHERE
            at >= ? AND at <= ?;
            """
        week_end = week_start + timedelta(days=6)
        res = self.cursor.execute(query, (week_start, week_end)).fetchall()

        lessons_list = lesson_to_list_retort.load(res, list[Lesson])

        for lesson in lessons_list:
            lesson.at = datetime.strptime(str(lesson.at), "%Y-%m-%d %H:%M:%S%z")

        lessons: dict[datetime, Lesson] = {lesson.at: lesson for lesson in lessons_list}

        week_lessons = WeekLessons(
            week_start=week_start,
            lessons=lessons,
            week_end=week_end,
        )

        return week_lessons

    def read_first_lessons_of_weeks(self) -> LessonsByDate:
        query = """
            SELECT *
            FROM Lesson
            WHERE strftime('%w', at) = '1';
            """
        res = self.cursor.execute(query).fetchall()

        lessons_list = lesson_to_list_retort.load(res, list[Lesson])

        for lesson in lessons_list:
            lesson.at = datetime.strptime(str(lesson.at), "%Y-%m-%d %H:%M:%S%z")

        lessons_by_date = LessonsByDate(
            lessons={lesson.at: lesson for lesson in lessons_list},
        )

        return lessons_by_date
