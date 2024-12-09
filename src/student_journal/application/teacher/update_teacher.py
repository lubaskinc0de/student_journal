from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.teacher import validate_teacher_invariants
from student_journal.domain.access_service.generic import StudentAccessService
from student_journal.domain.entity.teacher import Teacher
from student_journal.domain.id_type.teacher_id import TeacherId


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
    access: StudentAccessService[Teacher]

    def execute(self, data: UpdatedTeacher) -> TeacherId:
        with self.transaction_manager.begin():
            self.idp.ensure_auth()
            student_id = self.idp.get_id()

            validate_teacher_invariants(full_name=data.full_name)

            teacher = Teacher(
                teacher_id=data.teacher_id,
                full_name=data.full_name,
                avatar=data.avatar,
                student_id=student_id,
            )
            self.access.ensure_has_access(teacher)

            self.gateway.update_teacher(teacher)
            self.transaction_manager.commit()

        return data.teacher_id
