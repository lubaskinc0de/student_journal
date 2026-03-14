from dataclasses import dataclass
from uuid import uuid4

import structlog

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.validators.home_task import (
    validate_home_task,
)
from student_journal.domain.entity.home_task import HomeTask
from student_journal.domain.id_type.lesson_id import LessonId
from student_journal.domain.id_type.task_id import HomeTaskId

logger: Logger = structlog.get_logger(__name__)


@dataclass(slots=True, frozen=True)
class NewHomeTask:
    lesson_id: LessonId
    description: str
    is_done: bool = False


@dataclass(slots=True)
class CreateHomeTask:
    gateway: HomeTaskGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: NewHomeTask) -> HomeTaskId:
        self.idp.require_auth()

        validate_home_task(
            description=data.description,
        )
        task_id = HomeTaskId(uuid4())
        home_task = HomeTask(
            task_id=task_id,
            lesson_id=data.lesson_id,
            description=data.description,
            is_done=data.is_done,
            student_id=self.idp.get_student_id(),
        )

        with self.transaction_manager.begin():
            self.gateway.write_home_task(home_task)
            self.transaction_manager.commit()

        logger.debug(
            "Created new HomeTask",
            user_id=self.idp.get_student_id(),
            data=retort.dump(home_task),
        )
        return task_id
