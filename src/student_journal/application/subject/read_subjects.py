from dataclasses import dataclass

from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.models.subject import SubjectReadModel


@dataclass(slots=True)
class ReadSubjects:
    gateway: SubjectGateway

    def execute(self) -> list[SubjectReadModel]:
        subjects = self.gateway.read_subjects()
        return subjects
