from dataclasses import dataclass
from uuid import uuid4

from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.teacher import TeacherFullNameError
from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class NewTeacher:
    full_name: str


@dataclass(slots=True)
class CreateTeacher:
    gateway: TeacherGateway
    transaction_manager: TransactionManager

    def execute(self, data: NewTeacher) -> Teacher:
        if len(data.full_name) > 255:
            raise TeacherFullNameError()

        teacher_id = uuid4()
        teacher = Teacher(
            teacher_id=TeacherId(teacher_id),
            full_name=data.full_name,
        )

        self.transaction_manager.begin()
        self.gateway.write_teacher(teacher)
        self.transaction_manager.commit()

        return teacher
