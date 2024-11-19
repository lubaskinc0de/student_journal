from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.models.subject import SubjectReadModel


@dataclass(slots=True)
class ReadSubjects:
    gateway: SubjectGateway
    idp: IdProvider

    def execute(self) -> list[SubjectReadModel]:
        self.idp.ensure_is_auth()

        subjects = self.gateway.read_subjects()
        return subjects
