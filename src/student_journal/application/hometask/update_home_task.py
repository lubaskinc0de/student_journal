from dataclasses import dataclass

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.home_task import HomeTaskNotFoundError
from student_journal.application.invariants.home_task import (
    validate_home_task_invariants,
)
from student_journal.domain.entity.home_task import HomeTask
from student_journal.domain.id_type.lesson_id import LessonId
from student_journal.domain.id_type.task_id import HomeTaskId


@dataclass(slots=True, frozen=True)
class UpdatedHomeTask:
    task_id: HomeTaskId
    lesson_id: LessonId
    description: str
    is_done: bool = False


@dataclass(slots=True)
class UpdateHomeTask:
    gateway: HomeTaskGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: UpdatedHomeTask) -> HomeTaskId:
        self.idp.ensure_auth()

        validate_home_task_invariants(
            description=data.description,
        )

        with self.transaction_manager.begin():
            orig_object = self.gateway.read_home_task(data.task_id)

            if orig_object is None:
                raise HomeTaskNotFoundError

            home_task = HomeTask(
                task_id=data.task_id,
                lesson_id=data.lesson_id,
                description=data.description,
                is_done=data.is_done,
                student_id=orig_object.student_id,
            )

            self.gateway.update_home_task(home_task)
            self.transaction_manager.commit()

        return data.task_id
