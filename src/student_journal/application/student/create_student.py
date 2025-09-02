from dataclasses import dataclass
from uuid import uuid4

import structlog

from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.validators.student import validate_student
from student_journal.domain.entity.student import Student
from student_journal.domain.id_type.student_id import StudentId

logger: Logger = structlog.get_logger()


@dataclass(slots=True, frozen=True)
class NewStudent:
    age: int | None
    avatar: str | None
    name: str
    home_address: str | None


@dataclass(slots=True)
class CreateStudent:
    gateway: StudentGateway
    transaction_manager: TransactionManager

    def execute(self, data: NewStudent) -> StudentId:
        validate_student(
            age=data.age,
            name=data.name,
            home_address=data.home_address,
            avatar=data.avatar,
        )

        student_id = StudentId(uuid4())
        student = Student(
            student_id=student_id,
            avatar=data.avatar,
            age=data.age,
            name=data.name,
            home_address=data.home_address,
        )

        with self.transaction_manager.begin():
            self.gateway.write_student(student)
            self.transaction_manager.commit()

        logger.debug("Created new Student", data=retort.dump(student))
        return student_id
