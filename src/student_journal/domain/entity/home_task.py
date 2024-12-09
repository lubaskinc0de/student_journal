from dataclasses import dataclass

from student_journal.domain.id_type.lesson_id import LessonId
from student_journal.domain.id_type.student_id import StudentId
from student_journal.domain.id_type.task_id import HomeTaskId


@dataclass(slots=True)
class HomeTask:
    task_id: HomeTaskId
    lesson_id: LessonId
    student_id: StudentId
    description: str
    is_done: bool = False
