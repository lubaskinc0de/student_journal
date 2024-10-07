from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.models.teacher import TeachersReadModel


@dataclass(slots=True)
class ReadTeachers:
    gateway: TeacherGateway
    idp: IdProvider

    def execute(self) -> TeachersReadModel:
        student_id = self.idp.get_id()
        teachers = self.gateway.read_teachers(student_id)

        return TeachersReadModel(student_id=student_id, teachers=teachers)
