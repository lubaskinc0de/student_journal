from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.exceptions.subject import SubjectNotFoundError
from student_journal.domain.access_service.generic import StudentAccessService
from student_journal.domain.entity.subject import Subject
from student_journal.domain.id_type.subject_id import SubjectId


@dataclass(slots=True)
class ReadSubject:
    gateway: SubjectGateway
    idp: StudentIdProvider
    access: StudentAccessService[Subject]

    def execute(self, subject_id: SubjectId) -> Subject:
        self.idp.require_auth()
        subject = self.gateway.read_subject(subject_id)

        if not subject:
            raise SubjectNotFoundError

        self.access.ensure_has_access(subject)

        return subject
