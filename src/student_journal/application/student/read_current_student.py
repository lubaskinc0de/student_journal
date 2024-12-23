from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.converters.student import convert_student_to_read_model
from student_journal.application.models.student import StudentReadModel


@dataclass(slots=True)
class ReadCurrentStudent:
    gateway: StudentGateway
    idp: IdProvider

    def execute(self) -> StudentReadModel:
        current_student_id = self.idp.get_id()
        student = self.gateway.read_student(
            current_student_id,
        )

        avg = self.gateway.get_overall_avg_mark()
        return convert_student_to_read_model(student, avg, student.get_timezone())
