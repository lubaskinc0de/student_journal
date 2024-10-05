from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class NewSubject:
    teacher_id: TeacherId
    title: str


# TODO: кастомные классы исключений
@dataclass(slots=True)
class CreateSubject:
    gateway: SubjectGateway
    transaction_manager: TransactionManager

    def execute(self, data: NewSubject) -> Subject:
        if data.title and len(data.title) > 255:
            raise ValueError()

        subject_id = uuid4()
        subject = Subject(
            subject_id=SubjectId(subject_id),
            title=data.title,
            teacher_id=data.teacher_id,
        )

        self.transaction_manager.begin()
        self.gateway.write_subject(subject)
        self.transaction_manager.commit()

        return subject
