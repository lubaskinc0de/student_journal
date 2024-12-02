from dataclasses import dataclass

from student_journal.domain.lesson import Lesson
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.student_id import StudentId
from student_journal.domain.value_object.task_id import HomeTaskId


@dataclass(slots=True)
class HomeTaskReadModel:
    task_id: HomeTaskId
    lesson: Lesson
    subject: Subject
    description: str
    is_done: bool = False


@dataclass(slots=True)
class HomeTasksReadModel:
    student_id: StudentId
    home_tasks: list[HomeTaskReadModel]
