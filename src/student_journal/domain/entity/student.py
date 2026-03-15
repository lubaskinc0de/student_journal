from dataclasses import dataclass

from student_journal.domain.id_type.student_id import StudentId


@dataclass(slots=True)
class Student:
    student_id: StudentId
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None

    def can_view(self, student_id: StudentId) -> bool:
        return self.student_id == student_id
