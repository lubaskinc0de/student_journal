import logging
from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.id_type.subject_id import SubjectId


@dataclass(slots=True)
class DeleteSubject:
    transaction_manager: TransactionManager
    gateway: SubjectGateway
    idp: StudentIdProvider

    def execute(self, subject_id: SubjectId) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            self.gateway.delete_subject(subject_id)
            self.transaction_manager.commit()
        logging.debug("Deleted subject: %s", subject_id)
