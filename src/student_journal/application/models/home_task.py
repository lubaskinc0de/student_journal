from dataclasses import dataclass

from student_journal.domain.home_task import HomeTask
from student_journal.domain.value_object.student_id import StudentId


# домашнее задание
@dataclass(slots=True)
class HomeTasksReadModel:
    student_id: StudentId
    home_tasks: list[HomeTask]
