from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True)
class DeleteTeacher:
    transaction_manager: TransactionManager
    gateway: TeacherGateway
    idp: IdProvider

    def execute(self, teacher_id: TeacherId) -> None:
        self.idp.ensure_is_auth()

        with self.transaction_manager.begin():
            self.gateway.delete_teacher(teacher_id)
            self.transaction_manager.commit()
