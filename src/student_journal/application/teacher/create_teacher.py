from dataclasses import dataclass
from uuid import uuid4

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.validators.teacher import validate_teacher
from student_journal.domain.entity.teacher import Teacher
from student_journal.domain.id_type.teacher_id import TeacherId

logger: Logger = structlog.get_logger(__name__)


@dataclass(slots=True, frozen=True)
class NewTeacher:
    full_name: str
    avatar: str | None


@dataclass(slots=True)
class CreateTeacher:
    gateway: TeacherGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: NewTeacher) -> TeacherId:
        validate_teacher(full_name=data.full_name)

        with self.transaction_manager.begin():
            self.idp.require_auth()
            student_id = self.idp.get_student_id()

            teacher_id = TeacherId(uuid4())
            teacher = Teacher(
                teacher_id=teacher_id,
                full_name=data.full_name,
                avatar=data.avatar,
                student_id=student_id,
            )
            self.gateway.write_teacher(teacher)
            self.transaction_manager.commit()

            logger.debug(
                "Teacher created",
                data=retort.dump(teacher),
                user_id=self.idp.get_student_id(),
            )

        return teacher_id
