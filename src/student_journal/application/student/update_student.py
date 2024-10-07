from dataclasses import dataclass

from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.student import validate_student_invariants
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class UpdatedStudent:
    student_id: StudentId
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None
    timezone: int = 0


@dataclass(slots=True)
class UpdateStudent:
    gateway: StudentGateway
    transaction_manager: TransactionManager

    def execute(self, data: UpdatedStudent) -> StudentId:
        validate_student_invariants(
            age=data.age,
            name=data.name,
            home_address=data.home_address,
            timezone=data.timezone,
        )

        student = Student(
            student_id=data.student_id,
            avatar=data.avatar,
            age=data.age,
            name=data.name,
            home_address=data.home_address,
            timezone=data.timezone,
        )

        self.transaction_manager.begin()
        self.gateway.update_student(student)
        self.transaction_manager.commit()

        return data.student_id
