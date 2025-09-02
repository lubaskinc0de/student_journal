from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.id_type.lesson_id import LessonId


@dataclass(slots=True)
class DeleteLesson:
    transaction_manager: TransactionManager
    gateway: LessonGateway
    idp: StudentIdProvider

    def execute(self, lesson_id: LessonId) -> None:
        self.idp.require_auth()

        with self.transaction_manager.begin():
            self.gateway.delete_lesson(lesson_id)
            self.transaction_manager.commit()
