from dataclasses import dataclass
from datetime import datetime

from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.subject_id import SubjectId


# урок
@dataclass(slots=True)
class Lesson:
    lesson_id: LessonId
    subject_id: SubjectId
    at: datetime  # когда урок пройдет?
    mark: int | None  # оценка за урок
    note: str | None  # записка
    room: int  # кабинет
    index_number: int  # номер урока
