from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.transaction_manager import TransactionManager


@dataclass(frozen=True, slots=True)
class DeleteAllLessons:
    idp: IdProvider
    gateway: LessonGateway
    transaction_manager: TransactionManager

    def execute(self) -> None:
        self.idp.ensure_authenticated()
        with self.transaction_manager.begin():
            self.gateway.delete_all_lessons()
            self.transaction_manager.commit()
