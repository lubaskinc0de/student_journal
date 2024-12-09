from dataclasses import dataclass

from student_journal.domain.entity.teacher import Teacher
from student_journal.domain.id_type.subject_id import SubjectId


@dataclass(slots=True, frozen=True)
class SubjectReadModel:
    subject_id: SubjectId
    teacher: Teacher
    title: str
    avg_mark: float
    marks_list: list[int]
