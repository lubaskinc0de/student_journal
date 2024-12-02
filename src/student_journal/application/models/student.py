from dataclasses import dataclass
from datetime import timezone

from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class StudentReadModel:
    student_id: StudentId
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None
    student_overall_avg_mark: float
    time_zone: timezone
