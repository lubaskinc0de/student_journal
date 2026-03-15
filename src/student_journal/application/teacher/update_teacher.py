from dataclasses import dataclass

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.teacher import TeacherNotFoundError
from student_journal.application.validators.teacher import validate_teacher
from student_journal.domain.entity.teacher import Teacher
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.teacher_id import TeacherId

logger: Logger = structlog.get_logger(__name__)


@dataclass(slots=True, frozen=True)
class UpdatedTeacher:
    teacher_id: TeacherId
    full_name: str
    avatar: str | None


@dataclass(slots=True)
class UpdateTeacher:
    gateway: TeacherGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: UpdatedTeacher) -> TeacherId:
        validate_teacher(full_name=data.full_name)

        with self.transaction_manager.begin():
            self.idp.require_auth()
            orig_teacher = self.gateway.read_teacher(data.teacher_id)

            if orig_teacher is None:
                raise TeacherNotFoundError

            if not orig_teacher.can_manage(self.idp.get_student_id()):
                raise AccessDeniedError

            teacher = Teacher(
                teacher_id=data.teacher_id,
                full_name=data.full_name,
                avatar=data.avatar,
                student_id=orig_teacher.student_id,
            )

            self.gateway.update_teacher(teacher)
            self.transaction_manager.commit()

        logger.debug(
            "Updated Teacher",
            old_data=retort.dump(orig_teacher),
            data=retort.dump(teacher),
            user_id=self.idp.get_student_id(),
        )
        return data.teacher_id
