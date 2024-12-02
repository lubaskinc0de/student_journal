from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True)
class DeleteSubject:
    transaction_manager: TransactionManager
    gateway: SubjectGateway
    idp: IdProvider

    def execute(self, subject_id: SubjectId) -> None:
        self.idp.ensure_authenticated()

        with self.transaction_manager.begin():
            self.gateway.delete_subject(subject_id)
            self.transaction_manager.commit()
