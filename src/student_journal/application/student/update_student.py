from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.student import validate_student_invariants
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


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
    idp: IdProvider

    def execute(self, data: UpdatedStudent) -> StudentId:
        student = self.gateway.read_student(self.idp.get_id())

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

        with self.transaction_manager.begin():
            self.gateway.update_student(student)
            self.transaction_manager.commit()

        return student.student_id
