from dataclasses import dataclass
from datetime import datetime

from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True)
class Lesson:
    lesson_id: LessonId
    subject_id: SubjectId
    at: datetime
    mark: int | None
    note: str | None
    room: int
