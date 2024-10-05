from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.domain.student import Student


@dataclass(slots=True)
class ReadStudent:
    gateway: StudentGateway
    idp: IdProvider

    def execute(self) -> Student:
        current_student_id = self.idp.get_id()
        student = self.gateway.read_student(
            current_student_id,
        )  # TODO: обработать ошибку, когда студента нет.

        return student
