from datetime import UTC, datetime, timedelta

from student_journal.application.exceptions.lesson import (
    LessonAtError,
    LessonIndexNumberError,
    LessonMarkError,
    LessonNoteError,
    LessonRoomError,
)


def validate_lesson_at(at: datetime, student_timezone: int) -> None:
    if at < (datetime.now(tz=UTC) + timedelta(hours=student_timezone)):
        raise LessonAtError()


MARK_RANGE = range(1, 6)
NOTE_MAX_LENGTH = 65535
MIN_ROOM = 1
MIN_INDEX_NUMBER = 0


def validate_lesson_invariants(
    at: datetime,
    student_timezone: int,
    mark: int | None,
    note: str | None,
    room: int,
    index_number: int,
) -> None:
    validate_lesson_at(at, student_timezone)

    if mark and mark not in MARK_RANGE:
        raise LessonMarkError()

    if note and len(note) > NOTE_MAX_LENGTH:
        raise LessonNoteError()

    if room < MIN_ROOM:
        raise LessonRoomError()

    if index_number < MIN_INDEX_NUMBER:
        raise LessonIndexNumberError()
