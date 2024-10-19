from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.home_task import (
    validate_home_task_invariants,
)
from student_journal.domain.home_task import HomeTask
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.task_id import TaskId


@dataclass(slots=True, frozen=True)
class NewHomeTask:
    lesson_id: LessonId
    description: str
    is_done: bool = False


@dataclass(slots=True)
class CreateHomeTask:
    gateway: HomeTaskGateway
    transaction_manager: TransactionManager

    def execute(self, data: NewHomeTask) -> TaskId:
        validate_home_task_invariants(
            description=data.description,
        )
        task_id = TaskId(uuid4())
        home_task = HomeTask(
            task_id=task_id,
            lesson_id=data.lesson_id,
            description=data.description,
            is_done=data.is_done,
        )

        with self.transaction_manager.begin():
            self.gateway.write_home_task(home_task)
            self.transaction_manager.commit()

        return task_id
