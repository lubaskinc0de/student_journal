from dataclasses import dataclass

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.subject import SubjectNotFoundError
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.subject_id import SubjectId

logger: Logger = structlog.get_logger(__name__)


@dataclass(slots=True)
class DeleteSubject:
    transaction_manager: TransactionManager
    gateway: SubjectGateway
    idp: StudentIdProvider

    def execute(self, subject_id: SubjectId) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            subject = self.gateway.read_subject(subject_id)
            if subject is None:
                raise SubjectNotFoundError

            if not subject.can_manage(self.idp.get_student_id()):
                raise AccessDeniedError

            self.gateway.delete_subject(subject_id)
            self.transaction_manager.commit()

        logger.debug(
            "Deleted Subject",
            subject_id=subject_id,
            user_id=self.idp.get_student_id(),
        )
