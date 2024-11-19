from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.teacher import validate_teacher_invariants
from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class NewTeacher:
    full_name: str
    avatar: str | None


@dataclass(slots=True)
class CreateTeacher:
    gateway: TeacherGateway
    transaction_manager: TransactionManager
    idp: IdProvider

    def execute(self, data: NewTeacher) -> TeacherId:
        self.idp.ensure_is_auth()

        validate_teacher_invariants(full_name=data.full_name)

        teacher_id = TeacherId(uuid4())
        teacher = Teacher(
            teacher_id=teacher_id,
            full_name=data.full_name,
            avatar=data.avatar,
        )

        with self.transaction_manager.begin():
            self.gateway.write_teacher(teacher)
            self.transaction_manager.commit()

        return teacher_id
