from dataclasses import dataclass

from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True)
class Teacher:
    teacher_id: TeacherId
    full_name: str
    avatar: str | None
