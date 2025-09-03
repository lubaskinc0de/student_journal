from dataclasses import dataclass

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.exceptions.lesson import LessonNotFoundError
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.domain.entity.lesson import Lesson
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.lesson_id import LessonId


@dataclass(slots=True)
class ReadLesson:
    gateway: LessonGateway
    student_gateway: StudentGateway
    idp: StudentIdProvider

    def execute(self, lesson_id: LessonId) -> Lesson:
        self.idp.require_auth()
        student = self.student_gateway.read_student(self.idp.get_student_id())

        if not student:
            raise StudentNotFoundError

        lesson = self.gateway.read_lesson(lesson_id, student.get_timezone())

        if not lesson:
            raise LessonNotFoundError

        if not lesson.can_view(self.idp.get_student_id()):
            raise AccessDeniedError

        return lesson
