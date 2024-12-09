from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.exceptions.subject import SubjectNotFoundError
from student_journal.domain.entity.subject import Subject
from student_journal.domain.id_type.subject_id import SubjectId


@dataclass(slots=True)
class ReadSubject:
    gateway: SubjectGateway
    idp: StudentIdProvider

    def execute(self, subject_id: SubjectId) -> Subject:
        self.idp.ensure_auth()
        subject = self.gateway.read_subject(subject_id)

        if not subject:
            raise SubjectNotFoundError

        return subject
