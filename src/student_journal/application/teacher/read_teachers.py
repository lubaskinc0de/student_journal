from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.domain.entity.teacher import Teacher


@dataclass(slots=True)
class ReadTeachers:
    gateway: TeacherGateway
    idp: StudentIdProvider

    def execute(self) -> list[Teacher]:
        student_id = self.idp.get_student_id()
        teachers = self.gateway.read_teachers(student_id)
        return teachers
