from dataclasses import dataclass

from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.converters.student import convert_student_to_read_model
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.models.student import StudentReadModel
from student_journal.domain.id_type.student_id import StudentId


@dataclass(slots=True)
class ReadStudent:
    gateway: StudentGateway

    def execute(self, student_id: StudentId) -> StudentReadModel:
        student = self.gateway.read_student(
            student_id,
        )

        if not student:
            raise StudentNotFoundError

        avg = self.gateway.get_overall_avg_mark()
        return convert_student_to_read_model(student, avg, student.get_timezone())
