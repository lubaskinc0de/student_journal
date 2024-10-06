from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentHomeAddressError,
    StudentNameError,
    StudentTimezoneError,
)
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class NewStudent:
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None
    timezone: int


@dataclass(slots=True)
class CreateStudent:
    gateway: StudentGateway
    transaction_manager: TransactionManager

    def execute(self, data: NewStudent) -> StudentId:
        if data.age and data.age not in range(6, 100):
            raise StudentAgeError()

        if len(data.name) > 255:
            raise StudentNameError()

        if data.home_address and len(data.home_address) > 255:
            raise StudentHomeAddressError()

        if data.timezone and data.timezone not in range(24):
            raise StudentTimezoneError()

        student_id = StudentId(uuid4())
        student = Student(
            student_id=student_id,
            avatar=data.avatar,
            age=data.age,
            name=data.name,
            home_address=data.home_address,
            timezone=data.timezone,
        )

        self.transaction_manager.begin()
        self.gateway.write_student(student)
        self.transaction_manager.commit()

        return student_id
