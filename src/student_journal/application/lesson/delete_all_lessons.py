from dataclasses import dataclass

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.logger import Logger
from student_journal.application.common.transaction_manager import TransactionManager

logger: Logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class DeleteAllLessons:
    idp: StudentIdProvider
    gateway: LessonGateway
    transaction_manager: TransactionManager

    def execute(self) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            self.gateway.delete_all_lessons(self.idp.get_student_id())
            self.transaction_manager.commit()

        logger.debug("Deleted all lessons", user_id=self.idp.get_student_id())
