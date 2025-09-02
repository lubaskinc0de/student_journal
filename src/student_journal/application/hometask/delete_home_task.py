from dataclasses import dataclass

import structlog

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.home_task import HomeTaskNotFoundError
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.task_id import HomeTaskId

logger: Logger = structlog.get_logger()


@dataclass(slots=True)
class DeleteHomeTask:
    transaction_manager: TransactionManager
    gateway: HomeTaskGateway
    idp: StudentIdProvider

    def execute(self, task_id: HomeTaskId) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            obj = self.gateway.read_home_task(task_id)
            if obj is None:
                raise HomeTaskNotFoundError

            if not obj.can_manage(self.idp.get_student_id()):
                raise AccessDeniedError

            self.gateway.delete_home_task(task_id)
            self.transaction_manager.commit()

        logger.debug(
            "Deleted HomeTask",
            task_id=task_id,
            user_id=self.idp.get_student_id(),
        )
