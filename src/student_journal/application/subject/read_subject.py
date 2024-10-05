from dataclasses import dataclass

from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True)
class ReadSubject:
    gateway: SubjectGateway

    def execute(self, subject_id: SubjectId) -> Subject:
        subject = self.gateway.read_subject(subject_id)
        return subject
