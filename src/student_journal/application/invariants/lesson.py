from student_journal.application.exceptions.lesson import (
    LessonMarkError,
    LessonNoteError,
    LessonRoomError,
)

MIN_MARK = 1
MAX_MARK = 5
MARK_RANGE = range(MIN_MARK, MAX_MARK + 1)
NOTE_MAX_LENGTH = 65535
NOTE_MIN_LENGTH = 1
MIN_ROOM = 1


def validate_lesson_invariants(
    mark: int | None,
    note: str | None,
    room: int,
) -> None:
    if (mark is not None) and mark not in MARK_RANGE:
        raise LessonMarkError

    if (note is not None) and (
        len(note) > NOTE_MAX_LENGTH or len(note) < NOTE_MIN_LENGTH
    ):
        raise LessonNoteError

    if room < MIN_ROOM:
        raise LessonRoomError
