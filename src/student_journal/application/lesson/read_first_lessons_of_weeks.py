from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.tz import TimezoneProvider
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.models.lesson import LessonsByDate


@dataclass(slots=True, frozen=True)
class ReadFirstLessonsOfWeeks:
    gateway: LessonGateway
    student_gateway: StudentGateway
    idp: StudentIdProvider
    tz: TimezoneProvider

    def execute(self, month: int, year: int) -> LessonsByDate:
        self.idp.require_auth()

        student = self.student_gateway.read_student(self.idp.get_student_id())

        if not student:
            raise StudentNotFoundError

        return self.gateway.read_first_lessons_of_weeks(
            month,
            year,
            as_tz=self.tz.get_timezone(),
            student_id=student.student_id,
        )
