from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta, timezone
from sqlite3 import Cursor
from uuid import UUID

from student_journal.adapters.converter import lesson_retort, lesson_to_list_retort
from student_journal.adapters.converter.subject import subject_retort
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.exceptions.lesson import LessonNotFoundError
from student_journal.application.models.lesson import LessonsByDate, WeekLessons
from student_journal.domain.lesson import Lesson
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.lesson_id import LessonId


@dataclass(slots=True, frozen=True)
class SQLiteLessonGateway(LessonGateway):
    cursor: Cursor

    def read_lesson(self, lesson_id: LessonId, as_tz: timezone) -> Lesson:
        query = """
            SELECT lesson_id, subject_id, at, mark, note, room
            FROM Lesson WHERE lesson_id = ?
            """
        res = self.cursor.execute(query, (str(lesson_id),)).fetchone()

        if not res:
            raise LessonNotFoundError

        lesson = lesson_retort.load(dict(res), Lesson)
        lesson.at = lesson.at.astimezone(as_tz)

        return lesson

    def write_lesson(self, lesson: Lesson) -> None:
        query = """
            INSERT INTO Lesson
            (lesson_id, subject_id, at, mark, note, room)
            VALUES (?, ?, ?, ?, ?, ?)
            """

        lesson = Lesson(
            subject_id=lesson.subject_id,
            at=lesson.at.astimezone(UTC),
            mark=lesson.mark,
            note=lesson.note,
            room=lesson.room,
            lesson_id=lesson.lesson_id,
        )

        params = lesson_to_list_retort.dump(lesson)
        self.cursor.execute(query, params)

    def update_lesson(self, lesson: Lesson) -> None:
        query = """
            UPDATE Lesson SET
            subject_id = ?, at = ?, mark = ?, note = ?, room = ?
            WHERE lesson_id = ?
            """

        lesson = Lesson(
            subject_id=lesson.subject_id,
            at=lesson.at.astimezone(UTC),
            mark=lesson.mark,
            note=lesson.note,
            room=lesson.room,
            lesson_id=lesson.lesson_id,
        )

        params = lesson_to_list_retort.dump(lesson)
        params.append(params.pop(0))

        self.cursor.execute(query, params)

    def delete_lesson(self, lesson_id: LessonId) -> None:
        query = """
            DELETE FROM Lesson
            WHERE lesson_id = ?
            """
        self.cursor.execute(query, (str(lesson_id),))

    def read_lessons_for_week(self, week_start: date, as_tz: timezone) -> WeekLessons:
        query = """
        SELECT * FROM Lesson
        WHERE at >= DATETIME(:week_start) AND at < DATETIME(:week_end);
        """

        week_start = datetime.combine(
            week_start,
            datetime.min.time(),
            tzinfo=as_tz,
        ).astimezone(UTC)

        week_end = datetime.combine(
            week_start + timedelta(days=6),
            datetime.max.time(),
            tzinfo=as_tz,
        ).astimezone(UTC)

        params = {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
        }

        res = self.cursor.execute(query, params).fetchall()

        lessons_list = lesson_retort.load(
            [dict(row) for row in res],
            list[Lesson],
        )

        for lesson in lessons_list:
            lesson.at = datetime.strptime(
                str(lesson.at),
                "%Y-%m-%d %H:%M:%S%z",
            ).astimezone(as_tz)

        lessons: dict[date, list[Lesson]] = {}

        for lesson in lessons_list:
            lessons.setdefault(lesson.at.date(), []).append(lesson)

        for da_te, lesson_lst in lessons.items():
            lessons[da_te] = sorted(
                lesson_lst,
                key=lambda each: each.at,
            )

        week_lessons = WeekLessons(
            week_start=week_start,
            lessons=lessons,
            week_end=week_end,
        )

        return week_lessons

    def read_first_lessons_of_weeks(
        self,
        month: int,
        year: int,
        as_tz: timezone,
    ) -> LessonsByDate:
        query = """
            SELECT l.*
            FROM Lesson l
            JOIN (
                SELECT strftime('%Y-%W', at) AS week_year,
                       MIN(at) AS first_lesson_time
                FROM Lesson
                WHERE strftime('%Y', at) = :year
                  AND strftime('%m', at) = :month
                GROUP BY week_year
            ) grouped_lessons
            ON strftime('%Y-%W', l.at) = grouped_lessons.week_year
            AND l.at = grouped_lessons.first_lesson_time;
        """

        params = {
            "year": str(year),
            "month": f"{month:02}",
        }

        res = self.cursor.execute(query, params).fetchall()

        entries = [dict(row) for row in res]
        lessons_list = lesson_retort.load(entries, list[Lesson])

        for lesson in lessons_list:
            lesson.at = datetime.strptime(
                str(lesson.at),
                "%Y-%m-%d %H:%M:%S%z",
            ).astimezone(as_tz)

        lessons_by_date = LessonsByDate(
            lessons={lesson.at: lesson for lesson in lessons_list},
        )

        return lessons_by_date

    def read_subjects_for_lessons(
        self,
        lessons: list[LessonId],
    ) -> dict[LessonId, Subject]:
        query = """
        SELECT Lesson.lesson_id as lesson_id, Subject.*
        FROM Lesson
        JOIN Subject ON Lesson.subject_id = Subject.subject_id
        WHERE Lesson.lesson_id IN ({placeholders})
        """

        placeholders = ",".join("?" for _ in lessons)
        query = query.format(placeholders=placeholders)

        params = [str(lesson) for lesson in lessons]

        res = self.cursor.execute(query, params).fetchall()

        output = {}

        for entry in res:
            entry_d = dict(entry)
            lesson_id = LessonId(UUID(entry_d.pop("lesson_id")))
            subject = subject_retort.load(entry_d, Subject)

            output[lesson_id] = subject

        return output

    def delete_lessons(self, lessons: list[LessonId]) -> None:
        query = """
        DELETE FROM Lesson WHERE lesson_id IN ({placeholders})
        """

        placeholders = ",".join("?" for _ in lessons)
        query = query.format(placeholders=placeholders)

        params = [str(lesson) for lesson in lessons]

        self.cursor.execute(query, params)

    def delete_all_lessons(self) -> None:
        query = """
        DELETE FROM Lesson
        """

        self.cursor.execute(query)
