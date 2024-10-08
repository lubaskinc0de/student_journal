from dataclasses import dataclass

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.home_task import (
    validate_home_task_invariants,
)
from student_journal.domain.home_task import HomeTask
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.task_id import TaskId


@dataclass(slots=True, frozen=True)
class UpdatedHomeTask:
    task_id: TaskId
    lesson_id: LessonId
    description: str
    is_done: bool = False


@dataclass(slots=True)
class UpdateHomeTask:
    gateway: HomeTaskGateway
    transaction_manager: TransactionManager

    def execute(self, data: UpdatedHomeTask) -> TaskId:
        self.transaction_manager.begin()

        validate_home_task_invariants(
            description=data.description,
        )

        home_task = HomeTask(
            task_id=data.task_id,
            lesson_id=data.lesson_id,
            description=data.description,
            is_done=data.is_done,
        )

        self.gateway.update_home_task(home_task)
        self.transaction_manager.commit()

        return data.task_id
