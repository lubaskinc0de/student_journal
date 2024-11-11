from datetime import datetime
from sqlite3 import Cursor

import pytest
from unit.conftest import (
    LESSON,
    LESSON_ID,
    LESSON_MONDAY,
    LESSON_MONDAY_2,
    SUBJECT_ID,
    student_timezone,
)

from student_journal.adapters.models.lesson import lesson_retort
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.exceptions.lesson import LessonDoesNotExistError
from student_journal.domain.lesson import Lesson

READ_LESSON_SQL = "SELECT * FROM Lesson"
READ_WEEK_LESSON_SQL = """
    SELECT * FROM Lesson
    WHERE
    at >= ? AND at <= ?;
    """
READ_FIRST_LESSONS_OF_WEEK_SQL = """
    SELECT *
    FROM Lesson
    WHERE strftime('%w', at) = '1';
    """


def test_write(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    lesson_gateway.write_lesson(LESSON)
    db_lesson = lesson_retort.load(
        dict(cursor.execute(READ_LESSON_SQL).fetchone()),
        Lesson,
    )

    assert db_lesson == LESSON


def test_read(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    lesson_gateway.write_lesson(LESSON)
    db_lesson = lesson_retort.load(
        dict(cursor.execute(READ_LESSON_SQL).fetchone()),
        Lesson,
    )
    assert db_lesson == lesson_gateway.read_lesson(LESSON_ID)


def test_read_not_exist(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    with pytest.raises(LessonDoesNotExistError):
        lesson_gateway.read_lesson(LESSON_ID)


def test_update(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    lesson_gateway.write_lesson(LESSON)
    updated_lesson = Lesson(
        lesson_id=LESSON_ID,
        subject_id=SUBJECT_ID,
        at=datetime(2023, 12, 11, tzinfo=student_timezone),
        mark=3,
        note="testtttt",
        room=5,
        index_number=3,
    )

    lesson_gateway.update_lesson(updated_lesson)
    db_lesson = lesson_retort.load(
        dict(cursor.execute(READ_LESSON_SQL).fetchone()),
        Lesson,
    )

    assert db_lesson == updated_lesson


def test_read_lessons_for_week(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    lesson_gateway.write_lesson(LESSON)
    lesson_gateway.write_lesson(LESSON_MONDAY)

    lessons_list = [
        dict(lesson)
        for lesson in cursor.execute(
            READ_WEEK_LESSON_SQL,
            (
                datetime(2024, 11, 11, tzinfo=student_timezone),
                datetime(2024, 11, 17, tzinfo=student_timezone),
            ),
        ).fetchall()
    ]

    db_lessons = lesson_retort.load(
        lessons_list,
        list[Lesson],
    )

    week_lessons_model = lesson_gateway.read_lessons_for_week(
        datetime(2024, 11, 11, tzinfo=student_timezone),
    )

    assert db_lessons == list(week_lessons_model.lessons.values())


def test_read_first_lessons_of_weeks(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    lesson_gateway.write_lesson(LESSON_MONDAY)
    lesson_gateway.write_lesson(LESSON_MONDAY_2)

    lessons_list = [
        dict(lesson)
        for lesson in cursor.execute(
            READ_FIRST_LESSONS_OF_WEEK_SQL,
        ).fetchall()
    ]

    db_lessons = lesson_retort.load(
        lessons_list,
        list[Lesson],
    )

    first_week_lessons = lesson_gateway.read_first_lessons_of_weeks()

    assert db_lessons == list(first_week_lessons.lessons.values())
