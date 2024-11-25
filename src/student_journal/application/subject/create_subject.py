from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.subject import validate_subject_invariants
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class NewSubject:
    teacher_id: TeacherId
    title: str


@dataclass(slots=True)
class CreateSubject:
    gateway: SubjectGateway
    transaction_manager: TransactionManager
    idp: IdProvider

    def execute(self, data: NewSubject) -> SubjectId:
        self.idp.ensure_authenticated()
        validate_subject_invariants(data.title)

        subject_id = SubjectId(uuid4())
        subject = Subject(
            subject_id=subject_id,
            title=data.title,
            teacher_id=data.teacher_id,
        )

        with self.transaction_manager.begin():
            self.gateway.write_subject(subject)
            self.transaction_manager.commit()

        return subject_id
