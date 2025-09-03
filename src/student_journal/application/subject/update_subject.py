from dataclasses import dataclass

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.subject import SubjectNotFoundError
from student_journal.application.validators.subject import validate_subject
from student_journal.domain.entity.subject import Subject
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.subject_id import SubjectId
from student_journal.domain.id_type.teacher_id import TeacherId

logger: Logger = structlog.get_logger()


@dataclass(slots=True, frozen=True)
class UpdatedSubject:
    subject_id: SubjectId
    teacher_id: TeacherId
    title: str


@dataclass(slots=True)
class UpdateSubject:
    gateway: SubjectGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: UpdatedSubject) -> SubjectId:
        validate_subject(data.title)

        with self.transaction_manager.begin():
            self.idp.require_auth()

            orig_subject = self.gateway.read_subject(data.subject_id)

            if orig_subject is None:
                raise SubjectNotFoundError

            if not orig_subject.can_manage(self.idp.get_student_id()):
                raise AccessDeniedError

            subject = Subject(
                subject_id=data.subject_id,
                title=data.title,
                teacher_id=data.teacher_id,
                student_id=orig_subject.student_id,
            )

            self.gateway.update_subject(subject)
            self.transaction_manager.commit()

        logger.debug(
            "Updated Subject",
            old_data=retort.dump(orig_subject),
            data=retort.dump(subject),
            user_id=self.idp.get_student_id(),
        )
        return data.subject_id
