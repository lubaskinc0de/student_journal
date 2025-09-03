from dataclasses import dataclass

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.validators.student import validate_student
from student_journal.domain.entity.student import Student
from student_journal.domain.id_type.student_id import StudentId

logger: Logger = structlog.get_logger()


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
        validate_student(
            age=data.age,
            name=data.name,
            home_address=data.home_address,
            avatar=data.avatar,
        )

        with self.transaction_manager.begin():
            orig_student = self.gateway.read_student(self.idp.get_student_id())

            if not orig_student:
                raise StudentNotFoundError

            student = Student(
                student_id=self.idp.get_student_id(),
                avatar=data.avatar,
                age=data.age,
                name=data.name,
                home_address=data.home_address,
            )

            self.gateway.update_student(student)
            self.transaction_manager.commit()

            logger.debug(
                "Student updated",
                old_data=retort.dump(orig_student),
                data=retort.dump(student),
                user_id=self.idp.get_student_id(),
            )

        return student.student_id
