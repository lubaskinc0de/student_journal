from dataclasses import dataclass
from datetime import date

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager


@dataclass(frozen=True, slots=True)
class DeleteLessonsForWeek:
    idp: IdProvider
    gateway: LessonGateway
    student_gateway: StudentGateway
    transaction_manager: TransactionManager

    def execute(self, week_start: date) -> None:
        self.idp.ensure_authenticated()
        student = self.student_gateway.read_student(self.idp.get_id())

        dates = self.gateway.read_lessons_for_week(
            week_start,
            as_tz=student.get_timezone(),
        )

        ids = []

        for each in dates.lessons.values():
            ids.extend([lesson.lesson_id for lesson in each])

        with self.transaction_manager.begin():
            self.gateway.delete_lessons(ids)
            self.transaction_manager.commit()
