from dataclasses import dataclass

from student_journal.domain.id_type.student_id import StudentId
from student_journal.domain.id_type.teacher_id import TeacherId


@dataclass(slots=True)
class Teacher:
    teacher_id: TeacherId
    student_id: StudentId
    full_name: str
    avatar: str | None

    def can_manage(self, student_id: StudentId) -> bool:
        return self.student_id == student_id

    def can_view(self, student_id: StudentId) -> bool:
        return self.student_id == student_id
