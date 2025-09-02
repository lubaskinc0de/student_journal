from dataclasses import dataclass
from datetime import UTC

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.logger import Logger
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.lesson import LessonNotFoundError
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.lesson_id import LessonId

logger: Logger = structlog.get_logger()


@dataclass(slots=True)
class DeleteLesson:
    transaction_manager: TransactionManager
    gateway: LessonGateway
    idp: StudentIdProvider

    def execute(self, lesson_id: LessonId) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            lesson = self.gateway.read_lesson(lesson_id, UTC)
            if lesson is None:
                raise LessonNotFoundError

            if not lesson.can_manage(self.idp.get_student_id()):
                raise AccessDeniedError

            self.gateway.delete_lesson(lesson_id)
            self.transaction_manager.commit()

        logger.debug("Deleted lesson", user_id=self.idp.get_student_id())
