from dataclasses import dataclass

import structlog

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.home_task import HomeTaskNotFoundError
from student_journal.application.validators.home_task import (
    validate_home_task,
)
from student_journal.domain.entity.home_task import HomeTask
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.lesson_id import LessonId
from student_journal.domain.id_type.task_id import HomeTaskId

logger: Logger = structlog.get_logger(__name__)


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
        self.idp.require_auth()

        validate_home_task(
            description=data.description,
        )

        with self.transaction_manager.begin():
            orig_object = self.gateway.read_home_task(data.task_id)

            if orig_object is None:
                raise HomeTaskNotFoundError

            if not orig_object.can_manage(self.idp.get_student_id()):
                raise AccessDeniedError

            home_task = HomeTask(
                task_id=data.task_id,
                lesson_id=data.lesson_id,
                description=data.description,
                is_done=data.is_done,
                student_id=orig_object.student_id,
            )

            self.gateway.update_home_task(home_task)
            self.transaction_manager.commit()

        logger.debug(
            "Updated HomeTask",
            old_data=retort.dump(orig_object),
            new_data=retort.dump(home_task),
            user_id=self.idp.get_student_id(),
        )
        return data.task_id
