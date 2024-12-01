from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.models.lesson import LessonsByDate


@dataclass(slots=True, frozen=True)
class ReadFirstLessonsOfWeeks:
    gateway: LessonGateway
    student_gateway: StudentGateway
    idp: IdProvider

    def execute(self, month: int, year: int) -> LessonsByDate:
        self.idp.ensure_authenticated()

        student = self.student_gateway.read_student(self.idp.get_id())
        return self.gateway.read_first_lessons_of_weeks(
            month,
            year,
            as_tz=student.get_timezone(),
        )
