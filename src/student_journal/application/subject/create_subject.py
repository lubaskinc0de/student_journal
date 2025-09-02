import logging
from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.subject import validate_subject_invariants
from student_journal.domain.entity.subject import Subject
from student_journal.domain.id_type.subject_id import SubjectId
from student_journal.domain.id_type.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class NewSubject:
    teacher_id: TeacherId
    title: str


@dataclass(slots=True)
class CreateSubject:
    gateway: SubjectGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: NewSubject) -> SubjectId:
        validate_subject_invariants(data.title)

        with self.transaction_manager.begin():
            self.idp.ensure_auth()

            subject_id = SubjectId(uuid4())
            subject = Subject(
                subject_id=subject_id,
                title=data.title,
                teacher_id=data.teacher_id,
                student_id=self.idp.get_id(),
            )

            self.gateway.write_subject(subject)
            self.transaction_manager.commit()
        logging.debug("Subject created: %s", subject.subject_id)
        return subject_id
