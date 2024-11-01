from dataclasses import dataclass

from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.subject import validate_subject_invariants
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class UpdatedSubject:
    subject_id: SubjectId
    teacher_id: TeacherId
    title: str


@dataclass(slots=True)
class UpdateSubject:
    gateway: SubjectGateway
    transaction_manager: TransactionManager

    def execute(self, data: UpdatedSubject) -> SubjectId:
        validate_subject_invariants(data.title)

        subject = Subject(
            subject_id=data.subject_id,
            title=data.title,
            teacher_id=data.teacher_id,
        )

        with self.transaction_manager.begin():
            self.gateway.update_subject(subject)
            self.transaction_manager.commit()

        return data.subject_id
