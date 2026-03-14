from dataclasses import dataclass

from student_journal.domain.id_type.student_id import StudentId
from student_journal.domain.id_type.subject_id import SubjectId
from student_journal.domain.id_type.teacher_id import TeacherId


# сам предмет урока (математика, русский)
@dataclass(slots=True)
class Subject:
    subject_id: SubjectId
    teacher_id: TeacherId
    title: str
    student_id: StudentId

    def can_manage(self, student_id: StudentId) -> bool:
        return self.student_id == student_id

    def can_view(self, student_id: StudentId) -> bool:
        return self.student_id == student_id
