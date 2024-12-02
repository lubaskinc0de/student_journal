from dataclasses import dataclass
from datetime import date

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.models.lesson import WeekLessons


@dataclass(slots=True, frozen=True)
class ReadLessonsForWeek:
    gateway: LessonGateway
    student_gateway: StudentGateway
    idp: IdProvider

    def execute(self, week_start: date) -> WeekLessons:
        self.idp.ensure_authenticated()
        student = self.student_gateway.read_student(self.idp.get_id())

        lessons_by_date = self.gateway.read_lessons_for_week(
            week_start,
            as_tz=student.get_timezone(),
        )

        return lessons_by_date
