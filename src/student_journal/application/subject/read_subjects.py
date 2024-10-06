from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.models.subject import SubjectsReadModel


@dataclass(slots=True)
class ReadSubjects:
    gateway: SubjectGateway
    idp: IdProvider

    def execute(self) -> SubjectsReadModel:
        student_id = self.idp.get_id()
        subjects = self.gateway.read_subjects(student_id)

        return SubjectsReadModel(
            student_id=student_id,
            subjects=subjects,
        )
