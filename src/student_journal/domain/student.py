from dataclasses import dataclass
from datetime import timedelta, timezone

from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True)
class Student:
    student_id: StudentId
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None
    utc_offset: int = 3

    def get_timezone(self) -> timezone:
        return timezone(timedelta(hours=self.utc_offset))
