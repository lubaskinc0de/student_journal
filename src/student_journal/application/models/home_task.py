from dataclasses import dataclass

from student_journal.domain.entity.lesson import Lesson
from student_journal.domain.entity.subject import Subject

from student_journal.domain.id_type.task_id import HomeTaskId


@dataclass(slots=True)
class HomeTaskReadModel:
    task_id: HomeTaskId
    lesson: Lesson
    subject: Subject
    description: str
    is_done: bool = False

