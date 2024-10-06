from dataclasses import dataclass

from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.task_id import TaskId


# домашнее задание
@dataclass(slots=True)
class HomeTask:
    task_id: TaskId
    lesson_id: LessonId
    description: str
    is_done: bool = False
