from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.student import validate_student_invariants
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class NewStudent:
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None
    timezone: int = 3


@dataclass(slots=True)
class CreateStudent:
    gateway: StudentGateway
    transaction_manager: TransactionManager

    def execute(self, data: NewStudent) -> StudentId:
        validate_student_invariants(
            age=data.age,
            name=data.name,
            home_address=data.home_address,
            avatar=data.avatar,
            timezone=data.timezone,
        )

        student_id = StudentId(uuid4())
        student = Student(
            student_id=student_id,
            avatar=data.avatar,
            age=data.age,
            name=data.name,
            home_address=data.home_address,
            timezone=data.timezone,
        )

        with self.transaction_manager.begin():
            self.gateway.write_student(student)
            self.transaction_manager.commit()

        return student_id
