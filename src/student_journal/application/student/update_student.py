import logging
from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.invariants.student import validate_student_invariants
from student_journal.domain.entity.student import Student
from student_journal.domain.id_type.student_id import StudentId


@dataclass(slots=True, frozen=True)
class UpdatedStudent:
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None


@dataclass(slots=True)
class UpdateStudent:
    gateway: StudentGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: UpdatedStudent) -> StudentId:
        with self.transaction_manager.begin():
            student = self.gateway.read_student(self.idp.get_id())

            if not student:
                raise StudentNotFoundError

            validate_student_invariants(
                age=data.age,
                name=data.name,
                home_address=data.home_address,
                avatar=data.avatar,
            )

            student = Student(
                student_id=self.idp.get_id(),
                avatar=data.avatar,
                age=data.age,
                name=data.name,
                home_address=data.home_address,
                utc_offset=student.utc_offset,
            )

            self.gateway.update_student(student)
            self.transaction_manager.commit()

            logging.debug("Student updated: %s", student.student_id)

        return student.student_id
