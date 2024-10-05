from dataclasses import dataclass

from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True)
class ReadTeacher:
    gateway: TeacherGateway

    def execute(self, teacher_id: TeacherId) -> Teacher:
        teacher = self.gateway.read_teacher(teacher_id)
        return teacher
