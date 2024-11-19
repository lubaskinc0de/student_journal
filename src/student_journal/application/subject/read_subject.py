from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True)
class ReadSubject:
    gateway: SubjectGateway
    idp: IdProvider

    def execute(self, subject_id: SubjectId) -> Subject:
        self.idp.ensure_is_auth()

        subject = self.gateway.read_subject(subject_id)
        return subject
