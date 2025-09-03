from dataclasses import dataclass

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.teacher import TeacherNotFoundError
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.teacher_id import TeacherId

logger: Logger = structlog.get_logger()


@dataclass(slots=True)
class DeleteTeacher:
    transaction_manager: TransactionManager
    gateway: TeacherGateway
    idp: StudentIdProvider

    def execute(self, teacher_id: TeacherId) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            teacher = self.gateway.read_teacher(teacher_id)

            if teacher is None:
                raise TeacherNotFoundError

            if not teacher.can_manage(self.idp.get_student_id()):
                raise AccessDeniedError

            self.gateway.delete_teacher(teacher_id)
            self.transaction_manager.commit()

        logger.debug(
            "Deleted Teacher: %s",
            teacher_id=teacher_id,
            user_id=self.idp.get_student_id(),
        )
