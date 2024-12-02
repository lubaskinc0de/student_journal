from datetime import UTC, datetime
from sqlite3 import Cursor

import pytest
from unit.conftest import (
    LESSON,
    LESSON_ID,
    LESSON_MONDAY,
    LESSON_MONDAY_2,
    LESSON_WEDNESDAY,
    SUBJECT_ID,
    student_timezone,
)

from student_journal.adapters.converter.lesson import lesson_retort
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.exceptions.lesson import LessonNotFoundError
from student_journal.domain.lesson import Lesson

READ_LESSON_SQL = "SELECT * FROM Lesson"

READ_WEEK_LESSONS_SQL = """
    SELECT * FROM Lesson
    WHERE at >= DATETIME(:week_start) AND at <= DATETIME(:week_end);
    """

READ_FIRST_LESSONS_OF_WEEK_SQL = """
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
    assert db_lesson == lesson_gateway.read_lesson(LESSON_ID, student_timezone)


def test_read_not_exist(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    with pytest.raises(LessonNotFoundError):
        lesson_gateway.read_lesson(LESSON_ID, student_timezone)


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
    lesson_gateway.write_lesson(LESSON_MONDAY)
    lesson_gateway.write_lesson(LESSON_WEDNESDAY)
    lesson_gateway.write_lesson(LESSON_MONDAY_2)

    week_start = datetime.combine(
        LESSON_MONDAY.at.date(),
        datetime.min.time(),
        tzinfo=student_timezone,
    ).astimezone(UTC)

    week_end = datetime.combine(
        LESSON_WEDNESDAY.at.date(),
        datetime.max.time(),
        tzinfo=student_timezone,
    ).astimezone(UTC)

    lessons_list = [
        dict(lesson)
        for lesson in cursor.execute(
            READ_WEEK_LESSONS_SQL,
            {
                "week_start": week_start,
                "week_end": week_end,
            },
        ).fetchall()
    ]

    db_lessons = lesson_retort.load(
        lessons_list,
        list[Lesson],
    )

    gateway_output = lesson_gateway.read_lessons_for_week(
        LESSON_MONDAY.at.date(),
        LESSON_MONDAY.at.tzinfo,
    )
    gateway_output_list = []

    for each in gateway_output.lessons.values():
        gateway_output_list.extend(each)

    assert len(gateway_output_list) == 2  # noqa: PLR2004
    assert gateway_output_list == db_lessons


def test_read_first_lessons_of_weeks(
    lesson_gateway: LessonGateway,
    cursor: Cursor,
) -> None:
    lesson_gateway.write_lesson(LESSON_MONDAY)
    lesson_gateway.write_lesson(LESSON_MONDAY_2)

    year = LESSON_MONDAY.at.date().year
    month = LESSON_MONDAY.at.date().month
    lessons_list = [
        dict(lesson)
        for lesson in cursor.execute(
            READ_FIRST_LESSONS_OF_WEEK_SQL,
            {
                "year": str(year),
                "month": f"{month:02}",
            },
        ).fetchall()
    ]

    db_lessons = lesson_retort.load(
        lessons_list,
        list[Lesson],
    )
    lessons_from_db = []

    for lesson in db_lessons:
        lesson.at = lesson.at.astimezone(student_timezone)
        lessons_from_db.append(lesson)

    gateway_output = lesson_gateway.read_first_lessons_of_weeks(
        month,
        year,
        student_timezone,
    )
    gateway_output_list = list(gateway_output.lessons.values())

    assert len(gateway_output_list) == 2  # noqa: PLR2004
    assert db_lessons == gateway_output_list
