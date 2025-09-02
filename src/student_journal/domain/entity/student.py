from dataclasses import dataclass
from datetime import timedelta, timezone

from student_journal.domain.id_type.student_id import StudentId


@dataclass(slots=True)
class Student:
    student_id: StudentId
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None

    def get_timezone(self) -> timezone:
        return timezone(timedelta(hours=self.utc_offset))
