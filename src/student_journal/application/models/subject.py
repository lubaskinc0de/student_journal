from dataclasses import dataclass

from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.student_id import StudentId
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True, frozen=True)
class SubjectReadModel:
    subject_id: SubjectId
    teacher: Teacher
    title: str
    avg_mark: float


@dataclass(slots=True, frozen=True)
class SubjectsReadModel:
    student_id: StudentId
    subjects: list[SubjectReadModel]
