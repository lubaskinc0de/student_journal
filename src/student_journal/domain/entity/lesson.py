from dataclasses import dataclass
from datetime import datetime

from student_journal.domain.id_type.lesson_id import LessonId
from student_journal.domain.id_type.student_id import StudentId
from student_journal.domain.id_type.subject_id import SubjectId


@dataclass(slots=True)
class Lesson:
    lesson_id: LessonId
    subject_id: SubjectId
    student_id: StudentId
    at: datetime
    mark: int | None
    note: str | None
    room: int

    def can_manage(self, student_id: StudentId) -> bool:
        return self.student_id == student_id

    def can_view(self, student_id: StudentId) -> bool:
        return self.student_id == student_id
