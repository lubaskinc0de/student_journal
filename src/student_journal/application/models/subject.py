from dataclasses import dataclass

from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True, frozen=True)
class SubjectReadModel:
    subject_id: SubjectId
    teacher: Teacher
    title: str
    avg_mark: float
