from dataclasses import dataclass

from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class TeachersReadModel:
    student_id: StudentId
    teachers: list[Teacher]
