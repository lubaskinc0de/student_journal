from dataclasses import dataclass

from student_journal.domain.value_object.teacher_id import TeacherId


# преподаватель
@dataclass(slots=True)
class Teacher:
    teacher_id: TeacherId
    full_name: str  # имя преподавателя
    avatar: str | None
