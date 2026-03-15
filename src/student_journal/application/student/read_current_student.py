from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.tz import TimezoneProvider
from student_journal.application.converters.student import convert_student_to_read_model
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.models.student import StudentReadModel


@dataclass(slots=True)
class ReadCurrentStudent:
    gateway: StudentGateway
    idp: StudentIdProvider
    tz: TimezoneProvider

    def execute(self) -> StudentReadModel:
        current_student_id = self.idp.get_student_id()
        student = self.gateway.read_student(
            current_student_id,
        )

        if not student:
            raise StudentNotFoundError

        avg = self.gateway.get_overall_avg_mark()
        return convert_student_to_read_model(student, avg, self.tz.get_timezone())
