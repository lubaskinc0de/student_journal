from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.exceptions.teacher import TeacherNotFoundError
from student_journal.domain.access_service.generic import StudentAccessService
from student_journal.domain.entity.teacher import Teacher
from student_journal.domain.id_type.teacher_id import TeacherId


@dataclass(slots=True)
class ReadTeacher:
    gateway: TeacherGateway
    access: StudentAccessService[Teacher]
    idp: StudentIdProvider

    def execute(self, teacher_id: TeacherId) -> Teacher:
        self.idp.ensure_auth()
        teacher = self.gateway.read_teacher(teacher_id)

        if not teacher:
            raise TeacherNotFoundError

        self.access.ensure_has_access(teacher)

        return teacher
