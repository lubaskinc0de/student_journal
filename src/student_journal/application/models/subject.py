from dataclasses import dataclass

from student_journal.domain.value_object.student_id import StudentId
from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class SubjectReadModel:
    subject_id: SubjectId
    teacher_id: TeacherId
    title: str
    avg_mark: float


@dataclass(slots=True, frozen=True)
class SubjectsReadModel:
    student_id: StudentId
    subjects: list[SubjectReadModel]
