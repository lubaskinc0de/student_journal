from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId


@dataclass(slots=True)
class ReadLesson:
    gateway: LessonGateway
    student_gateway: StudentGateway
    idp: IdProvider

    def execute(self, lesson_id: LessonId) -> Lesson:
        self.idp.ensure_authenticated()
        student = self.student_gateway.read_student(self.idp.get_id())
        lesson = self.gateway.read_lesson(lesson_id, student.get_timezone())
        return lesson
