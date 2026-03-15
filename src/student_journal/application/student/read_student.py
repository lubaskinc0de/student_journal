from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.tz import TimezoneProvider
from student_journal.application.converters.student import convert_student_to_read_model
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.models.student import StudentReadModel
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.student_id import StudentId


@dataclass(slots=True)
class ReadStudent:
    gateway: StudentGateway
    idp: StudentIdProvider
    tz: TimezoneProvider

    def execute(self, student_id: StudentId) -> StudentReadModel:
        student = self.gateway.read_student(
            student_id,
        )

        if not student:
            raise StudentNotFoundError

        if not student.can_view(student_id):
            raise AccessDeniedError

        avg = self.gateway.get_overall_avg_mark()
        return convert_student_to_read_model(student, avg, self.tz.get_timezone())
