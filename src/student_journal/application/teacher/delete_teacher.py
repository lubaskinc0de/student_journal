import logging
from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.id_type.teacher_id import TeacherId


@dataclass(slots=True)
class DeleteTeacher:
    transaction_manager: TransactionManager
    gateway: TeacherGateway
    idp: StudentIdProvider

    def execute(self, teacher_id: TeacherId) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            self.gateway.delete_teacher(teacher_id)
            self.transaction_manager.commit()
        logging.debug("Deleted teacher: %s", teacher_id)
