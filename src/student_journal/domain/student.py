from dataclasses import dataclass

from student_journal.domain.value_object.student_id import StudentId


# ученик
@dataclass(slots=True)
class Student:
    student_id: StudentId
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None  # домашний адрес
