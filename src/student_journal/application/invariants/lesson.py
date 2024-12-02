from datetime import UTC, datetime, timedelta

from student_journal.application.exceptions.lesson import (
    LessonInPastError,
    LessonMarkError,
    LessonNoteError,
    LessonRoomError,
)


def validate_lesson_at(at: datetime, student_timezone: int) -> None:
    if at < (datetime.now(tz=UTC) + timedelta(hours=student_timezone)):
        raise LessonInPastError


MIN_MARK = 1
MAX_MARK = 5
MARK_RANGE = range(MIN_MARK, MAX_MARK + 1)
NOTE_MAX_LENGTH = 65535
NOTE_MIN_LENGTH = 1
MIN_ROOM = 1


def validate_lesson_invariants(
    at: datetime,
    student_timezone: int,
    mark: int | None,
    note: str | None,
    room: int,
) -> None:
    validate_lesson_at(at, student_timezone)

    if (mark is not None) and mark not in MARK_RANGE:
        raise LessonMarkError

    if (note is not None) and (
        len(note) > NOTE_MAX_LENGTH or len(note) < NOTE_MIN_LENGTH
    ):
        raise LessonNoteError

    if room < MIN_ROOM:
        raise LessonRoomError
