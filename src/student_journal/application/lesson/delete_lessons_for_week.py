from dataclasses import dataclass
from datetime import date

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.logger import Logger
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.student import StudentNotFoundError

logger: Logger = structlog.get_logger()


@dataclass(frozen=True, slots=True)
class DeleteLessonsForWeek:
    idp: StudentIdProvider
    gateway: LessonGateway
    student_gateway: StudentGateway
    transaction_manager: TransactionManager

    def execute(self, week_start: date) -> None:
        self.idp.require_auth()
        student = self.student_gateway.read_student(self.idp.get_student_id())

        if not student:
            raise StudentNotFoundError

        dates = self.gateway.read_lessons_for_week(
            week_start,
            as_tz=student.get_timezone(),
            student_id=student.student_id,
        )

        ids = []

        for each in dates.lessons.values():
            ids.extend([lesson.lesson_id for lesson in each])

        with self.transaction_manager.begin():
            self.gateway.delete_lessons(ids)
            self.transaction_manager.commit()

        logger.debug(
            "Deleted lessons for week",
            user_id=self.idp.get_student_id(),
            week_start=week_start,
        )
