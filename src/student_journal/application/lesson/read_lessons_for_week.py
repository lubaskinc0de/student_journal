from dataclasses import dataclass
from datetime import date

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.tz import TimezoneProvider
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.models.lesson import WeekLessons


@dataclass(slots=True, frozen=True)
class ReadLessonsForWeek:
    gateway: LessonGateway
    student_gateway: StudentGateway
    idp: StudentIdProvider
    tz: TimezoneProvider

    def execute(self, week_start: date) -> WeekLessons:
        self.idp.require_auth()
        student = self.student_gateway.read_student(self.idp.get_student_id())

        if not student:
            raise StudentNotFoundError

        lessons_by_date = self.gateway.read_lessons_for_week(
            week_start,
            as_tz=self.tz.get_timezone(),
            student_id=student.student_id,
        )

        return lessons_by_date
