from dataclasses import dataclass

from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.domain.value_object.teacher_id import TeacherId


# сам предмет урока (математика, русский)
@dataclass(slots=True)
class Subject:
    subject_id: SubjectId
    teacher_id: TeacherId  # преподоаватель урока
    title: str  # название урока
