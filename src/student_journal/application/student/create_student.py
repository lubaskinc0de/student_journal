from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class NewStudent:
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None


# TODO: кастомные классы исключений
@dataclass(slots=True)
class CreateStudent:
    gateway: StudentGateway
    transaction_manager: TransactionManager

    def execute(self, data: NewStudent) -> Student:
        if data.age and data.age not in range(6, 100):
            raise ValueError()

        if len(data.name) > 255:
            raise ValueError()

        if data.home_address and len(data.home_address) > 255:
            raise ValueError()

        student_id = uuid4()
        student = Student(
            student_id=StudentId(student_id),
            avatar=data.avatar,
            age=data.age,
            name=data.name,
            home_address=data.home_address,
        )

        self.transaction_manager.begin()
        self.gateway.write_student(student)
        self.transaction_manager.commit()

        return student
