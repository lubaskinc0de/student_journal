from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.subject import SubjectNotFoundError
from student_journal.application.invariants.subject import validate_subject_invariants
from student_journal.domain.access_service.generic import StudentAccessService
from student_journal.domain.entity.subject import Subject
from student_journal.domain.id_type.subject_id import SubjectId
from student_journal.domain.id_type.teacher_id import TeacherId


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
    access: StudentAccessService[Subject]

    def execute(self, data: UpdatedSubject) -> SubjectId:
        with self.transaction_manager.begin():
            self.idp.ensure_auth()
            validate_subject_invariants(data.title)

            orig_subject = self.gateway.read_subject(data.subject_id)

            if orig_subject is None:
                raise SubjectNotFoundError

            self.access.ensure_has_access(orig_subject)
            subject = Subject(
                subject_id=data.subject_id,
                title=data.title,
                teacher_id=data.teacher_id,
                student_id=orig_subject.student_id,
            )

            self.gateway.update_subject(subject)
            self.transaction_manager.commit()

        return data.subject_id
